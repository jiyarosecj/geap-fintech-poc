from django.shortcuts import render
from django.http import HttpResponse
from .models import Evidence
import hashlib

def run_data_gate(request, loan_amount, age):
    # ലളിതമായ ലോജിക്: പ്രായം 18-ന് മുകളിൽ വേണം
    if age < 18:
        status = "FAIL"
        desc = "Underage applicant"
    else:
        status = "PASS"
        desc = "Age check passed"
    
    # എവിഡൻസ് ക്രിയേറ്റ് ചെയ്യുന്നു
    evidence = Evidence.objects.create(
        gate_name="Data Gate (DG)",
        status=status,
        evidence_hash=hashlib.sha256(desc.encode()).hexdigest(),
        description=desc
    )
    return HttpResponse(f"Gate Result: {status}")
# Create your views here.

def run_governance_gates(request):
    # സിമ്പിൾ ലോൺ അപേക്ഷാ ഡാറ്റ (PoC-യ്ക്ക് വേണ്ടി)
    # applicant = {"name": "Test User", "age": 25, "loan_amount": 50000}
    
    # # 5 ഗേറ്റുകളുടെ ലോജിക്
    # gates = [
    #     ("Data Gate", applicant["age"] >= 18, "Age verification"),
    #     ("Train Gate", True, "Model reproducibility check"),
    #     ("Validate Gate", True, "Fairness metric passed"),
    #     ("Risk Gate", applicant["loan_amount"] < 100000, "Credit score check"),
    #     ("Output Gate", True, "Bias audit complete")
    # ]
    accuracy_score = 0.85  # ഒരു മാതൃകാപരമായ സ്കോർ
    threshold = 0.80
    
    gates = [
        ("Data Gate", True, "Data integrity verified"),
        ("Train Gate", True, "Training parameters logged"),
        ("Validation Gate", accuracy_score >= threshold, f"Model accuracy {accuracy_score} >= {threshold}"),
        ("Risk Gate", True, "Compliance met"),
        ("Output Gate", True, "Audit log generated")
    ]
    
    # ഓരോ ഗേറ്റിന്റെയും ഫലം ഡാറ്റാബേസിലേക്ക് (Evidence Backbone) അയക്കുന്നു
    for name, success, desc in gates:
        status = "PASS" if success else "FAIL"
        Evidence.objects.create(
            gate_name=name,
            status=status,
            evidence_hash=hashlib.sha256(desc.encode()).hexdigest(),
            description=desc
        )
        
    return render(request, 'governance/dashboard.html', {'gates': gates})

import json
from django.http import JsonResponse

def generate_report(request):
    # ഡാറ്റാബേസിൽ നിന്നുള്ള എല്ലാ തെളിവുകളും എടുക്കുന്നു
    evidence_data = list(Evidence.objects.values('gate_name', 'status', 'description', 'timestamp'))
    
    # ഒരു JSON ഫയൽ ഡൗൺലോഡ് ചെയ്യാൻ തരുന്നു
    response = JsonResponse(evidence_data, safe=False)
    response['Content-Disposition'] = 'attachment; filename="conformity_bundle.json"'
    return response 
    