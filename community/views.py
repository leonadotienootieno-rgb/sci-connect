from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Resource, Topic, Post
from .forms import ResourceUploadForm, TopicCreateForm, PostCreateForm


# --- RESOURCE VIEWS ---
@login_required  # Resources should only be accessible to registered users
def resource_list_view(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    # Add filtering by category here if needed
    context = {'resources': resources, 'categories': Resource.RESOURCE_CATEGORIES}
    return render(request, 'resource_list.html', context)


@login_required
def resource_upload_view(request):
    # Optional: Only allow Mentors/Admins to upload high-quality resources
    # if not request.user.is_mentor and not request.user.is_superuser:
    #     return redirect('resource_list')

    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)  # Must include request.FILES for FileField
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            return redirect('resource_list')
    else:
        form = ResourceUploadForm()
    return render(request, 'resource_upload.html', {'form': form})


# --- DISCUSSION VIEWS ---
def topic_list_view(request):
    # Check for the filter parameter in the URL (e.g., /forum/?mentor=true)
    show_mentors_only = request.GET.get('mentor') == 'true'

    topics = Topic.objects.all().order_by('-created_at')

    if show_mentors_only:
        # Filter the topics to only include those created by a mentor
        topics = topics.filter(creator__is_mentor=True)

    context = {
        'topics': topics,
        'show_mentors_only': show_mentors_only,
    }
    return render(request, 'topic_list.html', context)


@login_required
def topic_detail_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.posts.all().order_by('created_at')

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            # Redirect to the same page to show the new post
            return redirect('topic_detail', topic_id=topic_id)
    else:
        form = PostCreateForm()

    return render(request, 'topic_detail.html', {'topic': topic, 'posts': posts, 'form': form})
def is_mentor_user(user):
    return user.is_authenticated and user.is_mentor
@user_passes_test(is_mentor_user)
def mentor_only_view(request):
    ...