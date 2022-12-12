from django.db.models import Q, Count
from django.db.models.functions import TruncDay
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Todo
from .serializes import TodoSerializer


class TodoCreateView(generics.CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class ListTodo(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'


class TodoFilterView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        month = self.request.GET.get('month')
        if query:
            qs = qs.filter(
                Q(title_icontains=query) |
                Q(description_icontains=query)
            )
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        if month:
            qs = qs.filter(created_at__month=month)

        return qs

    def filter_qs(self, date):
        qs = self.get_queryset().filter(deadline__contains=date)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        lst = qs.annotate(date=TruncDay('deadline')).values('date').annotate(count=Count('id'))
        print(lst)
        data = {
            "count": qs.count(),
            "results": []
        }
        for i in lst:
            data['results'].append({
                "date": i.get('date'),
                "count": i.get('count'),
                'competition': [
                    {'id': j.id, 'title': j.title} for j in self.filter_qs(i.get('date'))
                ]

            })

        return Response(data)
