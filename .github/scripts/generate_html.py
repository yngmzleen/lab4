#!/usr/bin/env python3
import os
import sys

def main():
    repo_name = sys.argv[1]
    tag = sys.argv[2]
    repo_full = sys.argv[3]
    
    versions_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Версии релизов</title>
<style>
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px 20px; margin: 0; }}
.container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }}
h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
.version-list {{ list-style: none; padding: 0; }}
.version-item {{ margin-bottom: 15px; }}
.version-link {{ display: block; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 10px; transition: transform 0.3s ease; font-weight: bold; text-align: center; }}
.version-link:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); }}
</style>
</head>
<body>
<div class="container">
<h1>📦 Доступные версии релизов</h1>
<ul class="version-list" id="versions"><li style="text-align: center; color: #666;">Загрузка версий...</li></ul>
</div>
<script>
fetch('https://api.github.com/repos/{repo_full}/git/trees/gh-pages?recursive=1')
.then(r => r.json())
.then(data => {{
const versions = [...new Set(data.tree.filter(item => item.path.includes('/v') && item.type === 'tree').map(item => item.path.split('/')[1]))].filter(v => v.startsWith('v')).sort().reverse();
const list = document.getElementById('versions');
if (versions.length === 0) {{
list.innerHTML = '<li style="text-align: center; color: #666;">Версии будут доступны после создания релизов</li>';
}} else {{
list.innerHTML = versions.map(version => '<li class="version-item"><a href="' + version + '/" class="version-link">🚀 Версия ' + version + '</a></li>').join('');
}}
}})
.catch(() => {{ document.getElementById('versions').innerHTML = '<li style="text-align: center; color: #666;">Ошибка загрузки версий</li>'; }});
</script>
</body>
</html>'''
    
    os.makedirs(f"deploy/{repo_name}", exist_ok=True)
    with open(f"deploy/{repo_name}/index.html", "w", encoding="utf-8") as f:
        f.write(versions_html)
    
    redirect_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={repo_name}/{tag}/index.html">
<title>Redirecting...</title>
</head>
<body>
<p>Redirecting to <a href="{repo_name}/{tag}/index.html">version {tag}</a>...</p>
</body>
</html>'''
    
    with open("deploy/index.html", "w", encoding="utf-8") as f:
        f.write(redirect_html)
    
    print(f"Generated HTML files for release {tag}")

if __name__ == "__main__":
    main()

