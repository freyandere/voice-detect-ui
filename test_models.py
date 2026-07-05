"""
Test script to verify models.py is updated
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path('E:/2.Projects/voice-detect-ui')))
sys.path.insert(0, str(pathlib.Path('E:/2.Projects/voice-detect-ui/src')))

# Remove cached modules
for mod in list(sys.modules.keys()):
    if 'models' in mod or 'main' in mod:
        del sys.modules[mod]

# Import fresh
from models import predict_emotion, predict_age_gender, predict_speaker_verification
import numpy as np

print("Testing models with fresh import...")
print(f"\npredict_emotion source:")
import inspect
print(inspect.getsource(predict_emotion))

sample1 = np.random.randn(1000).astype(np.float32)
sample2 = np.zeros(1000, dtype=np.float32)

result1 = predict_emotion(sample1, None)
result2 = predict_emotion(sample2, None)

print(f"\nResult 1: {result1}")
print(f"Result 2: {result2}")
print(f"Are they different? {result1 != result2}")

print("\nTesting predict_age_gender...")
res1 = predict_age_gender(sample1, None)
res2 = predict_age_gender(sample2, None)
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
print(f"Are they different? {res1 != res2}")

print("\nTesting predict_speaker_verification...")
res1 = predict_speaker_verification(sample1, None)
res2 = predict_speaker_verification(sample2, None)
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
print(f"Are they different? {res1 != res2}")
