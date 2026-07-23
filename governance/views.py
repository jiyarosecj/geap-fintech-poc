from django.shortcuts import render
from django.http import HttpResponse
from .models import Evidence
import hashlib

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
# Create your views here.

def run_governance_gates(request):
<<<<<<< HEAD
    
    # applicant = {"name": "Test User", "age": 25, "loan_amount": 50000}
    
    # # 5 
    # gates = [
    #     ("Data Gate", applicant["age"] >= 18, "Age verification"),
    #     ("Train Gate", True, "Model reproducibility check"),
    #     ("Validate Gate", True, "Fairness metric passed"),
    #     ("Risk Gate", applicant["loan_amount"] < 100000, "Credit score check"),
    #     ("Output Gate", True, "Bias audit complete")
    # ]
    accuracy_score = 0.85  
    threshold = 0.80
=======
    # അപേക്ഷകന്റെ ഡാറ്റയും മോഡലിന്റെ മെട്രിക്സും (ഇവിടെ വാല്യൂസ് മാറ്റി നിങ്ങൾക്ക് ടെസ്റ്റ് ചെയ്യാം)
    applicant = {
        "name": "Test User", 
        "age": 20,             # 18-ൽ കുറഞ്ഞാൽ Data Gate FAIL ആകും
        "loan_amount": 50000   # 100000-ൽ കൂടിയാൽ Risk Gate FAIL ആകും
    }
    
    model_data = {
        "is_reproducible": True,   # False ആയാൽ Train Gate FAIL ആകും
        "accuracy_score": 0.85,    # 0.8-ൽ കുറഞ്ഞാൽ Validation Gate FAIL ആകും
        "threshold": 0.80,
        "bias_detected": False     # True ആയാൽ Output Gate FAIL ആകും
    }
>>>>>>> bd1e95b (Updated views with full governance gates logic)
    
    # ഓരോ തവണ റൺ ചെയ്യുമ്പോഴും പഴയ ലോഗുകൾ ക്ലിയർ ചെയ്യാൻ
    Evidence.objects.all().delete()
    
    # 5 ഗേറ്റുകളുടെയും കൺട്രോൾ ലോജിക്
    gates = [
        # 1. Data Gate: പ്രായം പരിശോധിക്കുന്നു
        ("Data Gate", applicant["age"] >= 18, f"Age verification: {applicant['age']} (Required >= 18)"),
        
        # 2. Train Gate: മോഡൽ ആവർത്തിക്കാൻ കഴിയുന്നതാണോ (Reproducible) എന്ന് നോക്കുന്നു
        ("Train Gate", model_data["is_reproducible"], "Training parameters logged and reproducible"),
        
        # 3. Validation Gate: അക്യുറസി ചെക്ക് ചെയ്യുന്നു
        ("Validation Gate", model_data["accuracy_score"] >= model_data["threshold"], f"Model accuracy {model_data['accuracy_score']} >= {model_data['threshold']}"),
        
        # 4. Risk Gate: ലോൺ തുക കംപ്ലയൻസിനുള്ളിലാണോ എന്ന് നോക്കുന്നു
        ("Risk Gate", applicant["loan_amount"] <= 100000, f"Credit check: Loan amount {applicant['loan_amount']} <= 100000"),
        
        # 5. Output Gate: ഔട്ട്‌പുട്ടിൽ പക്ഷപാതം (Bias) ഉണ്ടോ എന്ന് പരിശോധിക്കുന്നു
        ("Output Gate", not model_data["bias_detected"], "Bias audit complete: No unfair bias detected")
    ]
    
<<<<<<< HEAD
    
=======
    # ഓരോ ഗേറ്റിന്റെയും ഫലം ഡാറ്റാബേസിലേക്ക് അയക്കുന്നു
>>>>>>> bd1e95b (Updated views with full governance gates logic)
    for name, success, desc in gates:
        status = "PASS" if success else "FAIL"
        Evidence.objects.create(
            gate_name=name,
            status=status,
            evidence_hash=hashlib.sha256(desc.encode()).hexdigest(),
            description=desc
        )
        
    # ഡാറ്റാബേസിൽ നിന്നുള്ള ലോഗുകൾ ഡാഷ്‌ബോർഡിലേക്ക് അയക്കുന്നു
    evidence_data = Evidence.objects.all().order_by('-timestamp')

    return render(request, 'governance/dashboard.html', {'gates': evidence_data})

import json
from django.http import JsonResponse

def generate_report(request):
   
    evidence_data = list(Evidence.objects.values('gate_name', 'status', 'description', 'timestamp'))
    
   
    response = JsonResponse(evidence_data, safe=False)
    response['Content-Disposition'] = 'attachment; filename="conformity_bundle.json"'
    return response 
    
