from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.db.models import Q, ProtectedError,Subquery, OuterRef
from django.core.paginator import Paginator
from .models import Fornitore, Magazzino, Mezzo, Tipologia, Zona, Listino, InserimentoFallito
from openpyxl import load_workbook
import pandas as pd
import json
import io
from django.http import HttpResponse
from django.core.files.base import ContentFile

from django.shortcuts import render
from django.contrib import messages
from .tools import *
from django.contrib.auth.decorators import user_passes_test
from datetime import date
from django.http import JsonResponse
from django.db.models import Sum, F
from django.db.models.functions import Coalesce


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from io import BytesIO
from .models import Prefattura, PrefatturaRighe
from django.db.models import Sum, F
from datetime import date
from django.utils import timezone

from userapp.models import UserSocieta