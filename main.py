from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# Custom User Model with roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('participant', 'Participant'),
        ('judge', 'Judge'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')

# Problem Model
class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=20)
    test_cases = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

# Submission Model
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Pending')
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.IntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(default=now)

# Leaderboard
class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

# Contest Model
class Contest(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    problems = models.ManyToManyField(Problem)
    participants = models.ManyToManyField(User)

# Plagiarism Detection (Simplified)
def check_plagiarism(submission_code, existing_codes):
    for code in existing_codes:
        if similarity(submission_code, code) > 80:
            return True
    return False

def similarity(code1, code2):
    return len(set(code1.split()) & set(code2.split())) / len(set(code1.split())) * 100

# API Endpoint for Submission
def submit_code(request):
    user = request.user
    problem_id = request.POST.get("problem_id")
    code = request.POST.get("code")
    language = request.POST.get("language")
    
    problem = Problem.objects.get(id=problem_id)
    submission = Submission.objects.create(
        user=user, problem=problem, code=code, language=language, status='Running'
    )
    
    # Code Execution Sandbox (Mocked)
    execution_result = execute_code_sandbox(code, problem.test_cases, language)
    submission.status = execution_result['status']
    submission.execution_time = execution_result['execution_time']
    submission.memory_used = execution_result['memory_used']
    submission.save()
    
    return JsonResponse({"status": submission.status})

def execute_code_sandbox(code, test_cases, language):
    # Simulating execution
    return {"status": "Accepted", "execution_time": 0.5, "memory_used": 1024}

# Admin Panel (Simplified)
from django.contrib import admin
admin.site.register(User)
admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(Leaderboard)
admin.site.register(Contest)
