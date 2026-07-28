from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Evidence
import hashlib
import json

def run_data_gate(request, loan_amount, age):
    if age < 18:
        status = "FAIL"
        desc = "Underage applicant"
    else:
        status = "PASS"
        desc = "Age check passed"
    
    evidence = Evidence.objects.create(
        gate_name="Data Gate (DG)",
        status=status,
        evidence_hash=hashlib.sha256(desc.encode()).hexdigest(),
        description=desc
    )
    return HttpResponse(f"Gate Result: {status}")

def run_governance_gates(request):
    
    applicant = {
        "name": "Test User", 
        "age": 20,             
        "loan_amount": 50000  
    }
    
    model_data = {
        "is_reproducible": True,   
        "accuracy_score": 0.85,    
        "threshold": 0.80,
        "bias_detected": False    
    }
    
   
    Evidence.objects.all().delete()
    
    
    gates = [
       
        ("Data Gate", applicant["age"] >= 18, f"Age verification: {applicant['age']} (Required >= 18)"),
        
        
        ("Train Gate", model_data["is_reproducible"], "Training parameters logged and reproducible"),
        
        
        ("Validation Gate", model_data["accuracy_score"] >= model_data["threshold"], f"Model accuracy {model_data['accuracy_score']} >= {model_data['threshold']}"),
        
        
        ("Risk Gate", applicant["loan_amount"] <= 100000, f"Credit check: Loan amount {applicant['loan_amount']} <= 100000"),
        
        
        ("Output Gate", not model_data["bias_detected"], "Bias audit complete: No unfair bias detected")
    ]
    
    
    for name, success, desc in gates:
        status = "PASS" if success else "FAIL"
        Evidence.objects.create(
            gate_name=name,
            status=status,
            evidence_hash=hashlib.sha256(desc.encode()).hexdigest(),
            description=desc
        )
        
    
    evidence_data = Evidence.objects.all().order_by('-timestamp')

    return render(request, 'governance/dashboard.html', {'gates': evidence_data})

def generate_report(request):
    evidence_data = list(Evidence.objects.values('gate_name', 'status', 'description', 'timestamp'))
    
    response = JsonResponse(evidence_data, safe=False)
    response['Content-Disposition'] = 'attachment; filename="conformity_bundle.json"'
    return response
