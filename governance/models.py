from django.db import models

class Evidence(models.Model):
    gate_name = models.CharField(max_length=50) # DG, TG, VG, RG, OG
    status = models.CharField(max_length=20)    # PASS, FAIL, WAIVER
    evidence_hash = models.CharField(max_length=64) # SHA-256 hash
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.gate_name} - {self.status}"