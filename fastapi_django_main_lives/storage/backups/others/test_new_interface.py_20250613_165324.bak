#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/workspaces/fastapi_django_main_live')

try:
    from mysite.routers.gradio import include_gradio_interfaces
    print('=== Testing NEW Interface Detection ===')
    interfaces, names = include_gradio_interfaces()
    print(f'Total detected interfaces: {len(interfaces)}')
    print(f'Interface names: {names}')
    print('=== Checking for weather interface ===')
    if 'weather' in names:
        print('✅ NEW weather interface detected successfully!')
        index = names.index('weather')
        print(f'Weather interface type: {type(interfaces[index])}')
    else:
        print('❌ Weather interface NOT detected')
        print('Available interfaces:', names)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
