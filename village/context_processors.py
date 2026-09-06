from .models import VisitCounter


def get_visit_count(request):
    """Get or create visit counter for the requested path"""
    path = request.path
    
    # Get or create counter for this path
    counter, created = VisitCounter.objects.get_or_create(
        path=path,
        defaults={'count': 0}
    )
    
    # Increment counter
    counter.count += 1
    counter.save()
    
    return {'visit_counter': counter}