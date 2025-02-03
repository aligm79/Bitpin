from posts.models import Comment, Post
from django.db.models import OuterRef, Count, Avg, Subquery
from django.db import transaction
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from scipy.stats import ks_2samp
from django.core.cache import cache


@shared_task(name="dirty_check")
def dirty_check():
        fifteen_seconds_ago = timezone.now() - timedelta(seconds=15)
        eight_days_ago = timezone.now() - timedelta(days=8)
        yesterday = timezone.now() - timedelta(days=1)

        last_7_days_history = cache.get("last_7_days_history")
        fresh_data = Comment.objects.filter(created_date__gte=fifteen_seconds_ago).defer("user", "is_dirty", "post")

        if not last_7_days_history:
                last_7_days_history = Comment.objects.filter(
                        created_date__gte=eight_days_ago,
                        created_date__lte=yesterday
                ).defer("user", "is_dirty", "post")

                cache.set("last_7_days_history", last_7_days_history, 24*60*60)

        last_7_days_points = list(last_7_days_history.values_list("point", flat=True))
        fresh_data_points = list(fresh_data.values_list("point", flat=True))

        _, p_value = ks_2samp(last_7_days_points, fresh_data_points)

        if p_value >= 0.05:     
                update_average_and_people_count.delay()
        else:
                fresh_data_ids = list(fresh_data.values_list("id", flat=True))
                Comment.objects.filter(id__in=fresh_data_ids).update(is_dirty=True)   

@shared_task(name="update_average_and_people_count")
def update_average_and_people_count():
        fifteen_seconds_ago = timezone.now() - timedelta(seconds=15)
        subquery = Comment.objects.filter(
                is_dirty=False,
                post=OuterRef("id")).values("post").annotate(
                avg=Avg("point"), total_count=Count("id")).values("avg", "total_count")

        with transaction.atomic():
                Post.objects.prefetch_related("comment_set").filter(
                        comment__created_date__gte=fifteen_seconds_ago,
                        comment__is_dirty=False).select_for_update().update(
                        number_of_people=Subquery(subquery.values("total_count")),
                        avg_point=Subquery(subquery.values("avg")))