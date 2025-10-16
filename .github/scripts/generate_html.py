#!/usr/bin/env python3
import os
import sys
from datetime import datetime

def main():
    repo_name = sys.argv[1]
    tag = sys.argv[2]
    repo_full = sys.argv[3]
    
    # Страница со списком версий с улучшенным дизайном
    versions_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Версии релизов - {repo_name}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    min-height: 100vh; 
    padding: 40px 20px; 
}}
.container {{ 
    max-width: 900px; 
    margin: 0 auto; 
    background: white; 
    border-radius: 20px; 
    padding: 40px; 
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); 
}}
h1 {{ 
    color: #333; 
    text-align: center; 
    margin-bottom: 10px; 
    font-size: 2.5em; 
}}
.subtitle {{
    text-align: center;
    color: #666;
    margin-bottom: 30px;
    font-size: 1.1em;
}}
.search-box {{
    margin-bottom: 30px;
    text-align: center;
}}
.search-box input {{
    padding: 12px 20px;
    width: 100%;
    max-width: 400px;
    border: 2px solid #ddd;
    border-radius: 25px;
    font-size: 16px;
    transition: border-color 0.3s;
}}
.search-box input:focus {{
    outline: none;
    border-color: #667eea;
}}
.version-list {{ 
    list-style: none; 
    padding: 0; 
}}
.version-item {{ 
    margin-bottom: 15px;
    opacity: 0;
    animation: fadeIn 0.5s ease-out forwards;
}}
.version-item:nth-child(1) {{ animation-delay: 0.1s; }}
.version-item:nth-child(2) {{ animation-delay: 0.2s; }}
.version-item:nth-child(3) {{ animation-delay: 0.3s; }}
.version-item:nth-child(4) {{ animation-delay: 0.4s; }}
.version-item:nth-child(5) {{ animation-delay: 0.5s; }}
.version-link {{ 
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 25px; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    text-decoration: none; 
    border-radius: 12px; 
    transition: all 0.3s ease; 
    font-weight: bold; 
}}
.version-link:hover {{ 
    transform: translateY(-5px); 
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4); 
}}
.version-link .version-name {{
    font-size: 1.3em;
}}
.version-link .version-badge {{
    background: rgba(255, 255, 255, 0.2);
    padding: 5px 15px;
    border-radius: 15px;
    font-size: 0.9em;
}}
.latest-badge {{
    background: #ffd700 !important;
    color: #333 !important;
}}
.loading {{ 
    text-align: center; 
    color: #666; 
    padding: 20px;
}}
.error {{
    text-align: center;
    color: #e74c3c;
    padding: 20px;
}}
.stats {{
    display: flex;
    justify-content: space-around;
    margin-bottom: 30px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 12px;
}}
.stat-item {{
    text-align: center;
}}
.stat-number {{
    font-size: 2em;
    font-weight: bold;
    color: #667eea;
}}
.stat-label {{
    color: #666;
    font-size: 0.9em;
    margin-top: 5px;
}}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.back-button {{
    display: inline-block;
    margin-bottom: 20px;
    padding: 10px 20px;
    background: #f8f9fa;
    color: #333;
    text-decoration: none;
    border-radius: 8px;
    transition: background 0.3s;
}}
.back-button:hover {{
    background: #e9ecef;
}}
</style>
</head>
<body>
<div class="container">
<a href="../" class="back-button">← Назад на главную</a>
<h1>📦 Версии релизов</h1>
<p class="subtitle">Все доступные версии проекта {repo_name}</p>

<div class="stats">
    <div class="stat-item">
        <div class="stat-number" id="total-versions">0</div>
        <div class="stat-label">Всего версий</div>
    </div>
    <div class="stat-item">
        <div class="stat-number" id="latest-version">...</div>
        <div class="stat-label">Последняя версия</div>
    </div>
</div>

<div class="search-box">
    <input type="text" id="search-input" placeholder="🔍 Поиск версии...">
</div>

<ul class="version-list" id="versions">
    <li class="loading">Загрузка версий...</li>
</ul>
</div>

<script>
(function() {{
    const versionsList = document.getElementById('versions');
    const searchInput = document.getElementById('search-input');
    const totalVersionsEl = document.getElementById('total-versions');
    const latestVersionEl = document.getElementById('latest-version');
    let allVersions = [];
    
    // Загрузка версий
    fetch('https://api.github.com/repos/{repo_full}/git/trees/gh-pages?recursive=1')
        .then(r => r.json())
        .then(data => {{
            const versions = [...new Set(data.tree
                .filter(item => item.path.includes('/{repo_name}/v') && item.type === 'tree')
                .map(item => {{
                    const parts = item.path.split('/');
                    return parts.find(p => p && p.startsWith('v'));
                }}))].filter(v => v).sort((a, b) => {{
                    // Семантическое сортирование версий
                    const parseVersion = v => v.substring(1).split('.').map(Number);
                    const [aMajor, aMinor, aPatch] = parseVersion(a);
                    const [bMajor, bMinor, bPatch] = parseVersion(b);
                    return (bMajor - aMajor) || (bMinor - aMinor) || (bPatch - aPatch);
                }});
            
            allVersions = versions;
            totalVersionsEl.textContent = versions.length;
            latestVersionEl.textContent = versions[0] || 'Нет версий';
            
            displayVersions(versions);
        }})
        .catch(err => {{
            console.error('Ошибка загрузки версий:', err);
            versionsList.innerHTML = '<li class="error">❌ Ошибка загрузки версий</li>';
        }});
    
    function displayVersions(versions) {{
        if (versions.length === 0) {{
            versionsList.innerHTML = '<li class="loading">Версии будут доступны после создания релизов</li>';
            return;
        }}
        
        versionsList.innerHTML = versions.map((version, index) => {{
            const isLatest = index === 0;
            const badgeClass = isLatest ? 'latest-badge' : '';
            const badgeText = isLatest ? 'Последняя' : (versions.length - index) + ' из ' + versions.length;
            
            return '<li class="version-item">' +
                '<a href="' + version + '/" class="version-link">' +
                    '<span class="version-name">🚀 Версия ' + version + '</span>' +
                    '<span class="version-badge ' + badgeClass + '">' + badgeText + '</span>' +
                '</a>' +
            '</li>';
        }}).join('');
    }}
    
    // Поиск версий
    searchInput.addEventListener('input', function() {{
        const query = this.value.toLowerCase();
        const filtered = allVersions.filter(v => v.toLowerCase().includes(query));
        displayVersions(filtered);
    }});
}})();
</script>
</body>
</html>'''
    
    os.makedirs(f"deploy/{repo_name}", exist_ok=True)
    with open(f"deploy/{repo_name}/index.html", "w", encoding="utf-8") as f:
        f.write(versions_html)
    
    # Редирект на последнюю версию
    redirect_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={repo_name}/{tag}/index.html">
<title>Redirecting...</title>
<style>
body {{
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}}
.container {{
    text-align: center;
}}
.spinner {{
    border: 5px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top: 5px solid white;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}}
@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}
a {{
    color: white;
    text-decoration: underline;
}}
</style>
</head>
<body>
<div class="container">
    <h1>🚀 Перенаправление на версию {tag}</h1>
    <div class="spinner"></div>
    <p>Если автоматический переход не работает, <a href="{repo_name}/{tag}/index.html">нажмите здесь</a></p>
</div>
</body>
</html>'''
    
    with open("deploy/index.html", "w", encoding="utf-8") as f:
        f.write(redirect_html)
    
    print(f"✅ Generated HTML files for release {tag}")

if __name__ == "__main__":
    main()
