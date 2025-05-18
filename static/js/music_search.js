document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const levelFilter = document.getElementById('level-filter');
    const genreFilter = document.getElementById('genre-filter');
    const resultsList = document.getElementById('results-list');

    // 添加调试日志
    console.log("脚本已加载，DOM元素:", {
        searchInput,
        searchBtn,
        levelFilter,
        genreFilter,
        resultsList
    });

    // 搜索函数
    function performSearch() {
        const query = searchInput.value.trim();
        const level = levelFilter.value;
        const genre = genreFilter.value;

        console.log("执行搜索，参数:", { query, level, genre });

        // 显示加载状态
        resultsList.innerHTML = '<div class="loading">搜索中...</div>';

        // 构造查询参数
        const params = new URLSearchParams();
        if (query) params.append('q', query);
        if (level) params.append('level', level);
        if (genre) params.append('genre', genre);

        // 发送请求
        fetch(`/api/music/search?${params}`)
            .then(response => {
                console.log("收到响应:", response);
                if (!response.ok) {
                    throw new Error(`HTTP错误! 状态码: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("解析数据:", data);
                if (data.success) {
                    displayResults(data.results);
                } else {
                    throw new Error(data.error || '未知错误');
                }
            })
            .catch(error => {
                console.error('搜索失败:', error);
                resultsList.innerHTML = `
                    <div class="loading error">
                        搜索失败: ${error.message}<br>
                        <button onclick="window.location.reload()">重试</button>
                    </div>
                `;
            });
    }

    // 显示结果
    function displayResults(songs) {
        console.log("显示结果:", songs);
        if (!songs || songs.length === 0) {
            resultsList.innerHTML = '<div class="loading">没有找到匹配的歌曲</div>';
            return;
        }

        resultsList.innerHTML = songs.map(song => `
            <div class="song-item" onclick="window.location.href='/music/${song.id}'">
                <div class="song-title">${song.title}</div>
                <div class="song-artist">${song.artist}</div>
                <div class="song-level ${getLevelClass(song.level_value)}">
                    ${song.level_display}
                </div>
                <div class="song-bpm">${song.bpm}</div>
            </div>
        `).join('');
    }

    // 获取难度CSS类
    function getLevelClass(levelValue) {
        const level = parseFloat(levelValue) || 0;
        if (level >= 13) return 'level-ultra';
        if (level >= 10) return 'level-master';
        if (level >= 7) return 'level-expert';
        if (level >= 5) return 'level-advanced';
        return 'level-basic';
    }

    // 绑定事件
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') performSearch();
    });

    // 初始加载
    performSearch();
});