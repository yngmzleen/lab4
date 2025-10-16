#!/usr/bin/env python3
"""
Добавляет селектор версий и информацию о текущей версии в HTML файлы
"""
import os
import sys
import re

def add_version_selector(html_content, current_version, repo_name):
    """Добавляет селектор версий в HTML"""
    
    version_selector_html = f'''
    <div id="version-selector" style="position: fixed; top: 10px; right: 10px; background: white; padding: 10px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 1000;">
        <label for="version-select" style="font-weight: bold; margin-right: 5px;">Версия:</label>
        <select id="version-select" style="padding: 5px; border-radius: 4px; border: 1px solid #ddd;">
            <option value="current">Загрузка...</option>
        </select>
    </div>
    <script>
        (function() {{
            const currentVersion = '{current_version}';
            const repoName = '{repo_name}';
            const currentPath = window.location.pathname;
            const isRuPage = currentPath.includes('/ru/');
            const isEnPage = currentPath.includes('/en/');
            
            // Загружаем список версий
            fetch('https://api.github.com/repos/' + window.location.pathname.split('/')[1] + '/' + repoName + '/git/trees/gh-pages?recursive=1')
                .then(r => r.json())
                .then(data => {{
                    const versions = [...new Set(data.tree
                        .filter(item => item.path.includes('/' + repoName + '/v') && item.type === 'tree')
                        .map(item => {{
                            const parts = item.path.split('/');
                            return parts.find(p => p.startsWith('v'));
                        }}))].filter(v => v).sort().reverse();
                    
                    const select = document.getElementById('version-select');
                    select.innerHTML = '';
                    
                    versions.forEach(version => {{
                        const option = document.createElement('option');
                        option.value = version;
                        option.textContent = version + (version === currentVersion ? ' (текущая)' : '');
                        if (version === currentVersion) {{
                            option.selected = true;
                        }}
                        select.appendChild(option);
                    }});
                    
                    // Обработчик смены версии
                    select.addEventListener('change', function() {{
                        const selectedVersion = this.value;
                        let newPath = '/' + repoName + '/' + selectedVersion + '/';
                        
                        if (isRuPage) {{
                            newPath += 'ru/';
                        }} else if (isEnPage) {{
                            newPath += 'en/';
                        }}
                        
                        window.location.href = newPath;
                    }});
                }})
                .catch(err => {{
                    console.error('Ошибка загрузки версий:', err);
                    document.getElementById('version-select').innerHTML = '<option>Ошибка загрузки</option>';
                }});
        }})();
    </script>
    '''
    
    # Вставляем селектор перед закрывающим тегом </body>
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', version_selector_html + '\n</body>')
    
    return html_content

def add_version_badge(html_content, current_version):
    """Добавляет бейдж с текущей версией"""
    
    version_badge = f'''
    <div style="position: fixed; bottom: 10px; right: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 999;">
        📦 {current_version}
    </div>
    '''
    
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', version_badge + '\n</body>')
    
    return html_content

def process_html_file(file_path, current_version, repo_name):
    """Обрабатывает один HTML файл"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Добавляем селектор версий
        content = add_version_selector(content, current_version, repo_name)
        
        # Добавляем бейдж версии
        content = add_version_badge(content, current_version)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Обработан: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при обработке {file_path}: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: add_version_info.py <directory> <version>")
        sys.exit(1)
    
    directory = sys.argv[1]
    version = sys.argv[2]
    
    # Извлекаем имя репозитория из пути
    repo_name = directory.split('/')[1] if '/' in directory else 'lab4'
    
    print(f"Добавление информации о версии {version} в файлы директории {directory}")
    
    # Обрабатываем все HTML файлы
    processed = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if process_html_file(file_path, version, repo_name):
                    processed += 1
    
    print(f"\nВсего обработано файлов: {processed}")

if __name__ == "__main__":
    main()

