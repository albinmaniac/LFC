from celery import shared_task


@shared_task
def test_task():
    print("=" * 50)
    print("Celery is working successfully!")
    print("=" * 50)
    return "Success"
