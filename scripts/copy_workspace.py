import os
import shutil

src = 'tasks/2026-05-15_精密电阻测试板方案/CIMC-PCB-Workspace'
dst = 'CIMC-PCB-Workspace'

for root, dirs, files in os.walk(src):
    rel = os.path.relpath(root, src)
    tgt = dst if rel == '.' else os.path.join(dst, rel)
    os.makedirs(tgt, exist_ok=True)
    for f in files:
        if f.endswith(('.csv', '.txt', '.png', '.md')):
            shutil.copy2(os.path.join(root, f), os.path.join(tgt, f))

print('Done')
