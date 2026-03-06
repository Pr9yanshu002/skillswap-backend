
from django.urls import path
from .views import SessionListCreateView, SessionSlotCreateView, SessionUpdateView, SlotSelectView


urlPatterns = [
    path('sessions/', SessionListCreateView.as_view(), name='session-list-create'),
    path('sessions/<int:pk>/', SessionUpdateView.as_view(), name='session-update'),
    path('sessions/<int:pk>/slots/', SessionSlotCreateView.as_view(), name='session-slot-create'),
    path('slots/<int:pk>/select/', SlotSelectView.as_view(), name='slot-select'),
]