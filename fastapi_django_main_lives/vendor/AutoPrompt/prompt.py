# prompt: これを　subprocess で作成して
# python run_pipeline.py \
#     --prompt "Does this movie review contain a spoiler? answer Yes or No" \
#     --task_description "Assistant is an expert classifier that will classify a movie review, and let the user know if it contains a spoiler for the reviewed movie or not." \
#     --num_steps 30

import subprocess

command = [
    'python', 'run_pipeline.py',
    '--prompt', '丁寧なコンサルをしているか yes,noで答えて下さい',
    '--task_description', 'あなたは、金、ダイヤ、ブランドの査定をするコンサルタントです',
    '--num_steps', '10'
]

command3 = [
    'python', 'run_generation_pipeline.py',
    '--prompt', 'この映画レビューにはネタバレが含まれていますか？YesまたはNoで答えてください',
    '--task_description', 'アシスタントは、映画レビューを分類するエキスパートであり、レビューされた映画のネタバレが含まれているかどうかをユーザーに教えてくれます。',
    #'--num_steps', '30'
]

command2 = [
    'python', 'run_pipeline.py',
    '--prompt', 'この映画レビューにはネタバレが含まれていますか？YesまたはNoで答えてください',
    '--task_description', 'アシスタントは、映画レビューを分類するエキスパートであり、レビューされた映画のネタバレが含まれているかどうかをユーザーに教えてくれます。',
    '--num_steps', '30'
]

subprocess.run(command)