"""Frontend assets (HTML/CSS/JS) kept separate from main application code.

This module exposes HEAD_HTML which is a single string inserted into the page head.
Keeping it separate improves readability and allows unit tests / formatting tools
to focus on Python code without being cluttered by large string literals.
"""

HEAD_HTML = '''
        <script>
            (function(){
                try{
                    const mq = window.matchMedia('(prefers-color-scheme: dark)');
                    function applyTheme(dark){
                        try{ if(dark) document.body.classList.add('dark-mode'); else document.body.classList.remove('dark-mode'); }catch(e){}
                    }
                    applyTheme(mq.matches);
                    if(mq.addEventListener) mq.addEventListener('change', e => applyTheme(e.matches));
                    else if(mq.addListener) mq.addListener(e => applyTheme(e.matches));
                }catch(e){}
            })();
        </script>
        <style>
            /* Theme variables */
            :root{
                --bg: #ffffff;
                --surface: #ffffff;
                --card: #ffffff;
                --text: #1f2937;
                --muted: #6b7280;
                --accent: #2f86c2;
                --card-elev: rgba(15,23,42,0.05);
            }
            .dark-mode{
                --bg: #0b1220;
                --surface: #07101a;
                --card: #0f1724;
                --text: #e6eef6;
                --muted: #9aa7b6;
                --accent: #3aa0ff;
                --card-elev: rgba(255,255,255,0.03);
            }
            @media (prefers-color-scheme: dark) {
                :root{
                    --bg: #0b1220;
                    --surface: #07101a;
                    --card: #0f1724;
                    --text: #e6eef6;
                    --muted: #9aa7b6;
                    --accent: #3aa0ff;
                    --card-elev: rgba(255,255,255,0.03);
                }
            }
            html, body, #app, .q-app, .q-page, .q-page-container, .q-layout, .q-layout__section, .q-page__content, .q-layout__container, .q-layout__section--center { background: var(--bg) !important; color: var(--text) !important; }
            .q-header, .q-toolbar, .q-drawer, .q-drawer__content, .q-header__container, .q-toolbar__content { background: var(--bg) !important; color: var(--text) !important; }
            .q-header { border-bottom: 1px solid rgba(0,0,0,0.06); }
            .dark-mode .q-header { border-bottom: 1px solid rgba(255,255,255,0.03); }
            .q-page-container { padding: 0 !important; }
            body { margin: 0; overflow-x: hidden; }
            .rounded-borders { border-radius: 8px; }
            .compact-table .q-table__tbody td { padding-top: 6px; padding-bottom: 6px; }
            .header-bar { background: var(--accent); color: white; padding: 10px 16px; font-weight: 700; }
            .controls { padding: 12px 18px; display: flex; align-items: center; gap: 12px; background: transparent; }
            .controls { background: rgba(0,0,0,0.02); border-bottom: 1px solid rgba(15,23,42,0.04); }
            .dark-mode .controls { background: rgba(255,255,255,0.01); border-bottom: 1px solid rgba(255,255,255,0.03); }
            .table-card { width: calc(100% - 48px); max-width: none; margin: 12px 24px; background: var(--card); box-shadow: 0 1px 2px var(--card-elev); }
            .table-card .q-card__section { padding: 8px; }
            .compact-table table { table-layout: fixed; width: 100%; color: var(--text); }
            .compact-table thead th:nth-child(1), .compact-table tbody td:nth-child(1) { width: 8%; text-align: center; }
            .compact-table thead th:nth-child(2), .compact-table tbody td:nth-child(2) { width: 20%; }
            .compact-table thead th:nth-child(3), .compact-table tbody td:nth-child(3) { width: 20%; }
            .compact-table thead th:nth-child(4), .compact-table tbody td:nth-child(4) { width: 8%; text-align: center; }
            .compact-table thead th:nth-child(5), .compact-table tbody td:nth-child(5) { width: 44%; white-space: normal; overflow: hidden; text-overflow: ellipsis; }
            @media (min-width: 1200px) {
                .compact-table .q-table__tbody td { padding-top: 4px; padding-bottom: 4px; }
            }
            .q-table thead th { position: sticky; top: 0; background: var(--surface); z-index: 3; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
            .compact-table th, .compact-table td { color: var(--text) !important; background: transparent !important; font-weight: 500; opacity: 1 !important; }
            .compact-table .q-table__tbody td { padding-top: 10px; padding-bottom: 10px; border-bottom: 1px solid rgba(0,0,0,0.06); line-height: 1.25; }
            .dark-mode .compact-table .q-table__tbody td { border-bottom: 1px solid rgba(255,255,255,0.03); }
            .compact-table .q-table__tbody td:nth-child(5) { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
            .compact-table thead th { background: var(--surface); color: var(--text); font-weight: 700; }
            .dark-toggle { margin-left: 12px; }
            .table-card, .table-card .q-card__section, .q-card { background: var(--card) !important; color: var(--text) !important; }
            .q-card__section { padding: 12px !important; }
            .q-table, .q-table__container { background: transparent !important; }
            .compact-table th, .compact-table td { color: var(--text) !important; opacity: 1 !important; }
            .compact-table .q-table__tbody td { background: transparent !important; }
            .table-card { border: 1px solid rgba(15,23,42,0.06); }
            .dark-mode .table-card { border: 1px solid rgba(255,255,255,0.04); }
            .compact-table .q-table__tbody td { border-bottom: 1px solid rgba(0,0,0,0.04); }
            .dark-mode .compact-table .q-table__tbody td { border-bottom: 1px solid rgba(255,255,255,0.03); }
        </style>
    '''
"""Frontend assets (HTML/CSS/JS) kept separate from main application code.

This module exposes HEAD_HTML which is a single string inserted into the page head.
Keeping it separate improves readability and allows unit tests / formatting tools
to focus on Python code without being cluttered by large string literals.
"""

HEAD_HTML = '''
        <script>
            (function(){
                try{
                    const mq = window.matchMedia('(prefers-color-scheme: dark)');
                    function applyTheme(dark){
                        try{ if(dark) document.body.classList.add('dark-mode'); else document.body.classList.remove('dark-mode'); }catch(e){}
                    }
                    applyTheme(mq.matches);
                    if(mq.addEventListener) mq.addEventListener('change', e => applyTheme(e.matches));
                    else if(mq.addListener) mq.addListener(e => applyTheme(e.matches));
                }catch(e){}
            })();
        </script>
        <style>
            /* Theme variables */
            :root{
                --bg: #ffffff;
                --surface: #ffffff;
                --card: #ffffff;
                --text: #1f2937;
                --muted: #6b7280;
                --accent: #2f86c2;
                --card-elev: rgba(15,23,42,0.05);
            }
            .dark-mode{
                --bg: #0b1220;
                --surface: #07101a;
                --card: #0f1724;
                --text: #e6eef6;
                --muted: #9aa7b6;
                --accent: #3aa0ff;
                --card-elev: rgba(255,255,255,0.03);
            }
            @media (prefers-color-scheme: dark) {
                :root{
                    --bg: #0b1220;
                    --surface: #07101a;
                    --card: #0f1724;
                    --text: #e6eef6;
                    --muted: #9aa7b6;
                    --accent: #3aa0ff;
                    --card-elev: rgba(255,255,255,0.03);
                }
            }
            html, body, #app, .q-app, .q-page, .q-page-container, .q-layout, .q-layout__section, .q-page__content, .q-layout__container, .q-layout__section--center { background: var(--bg) !important; color: var(--text) !important; }
            .q-header, .q-toolbar, .q-drawer, .q-drawer__content, .q-header__container, .q-toolbar__content { background: var(--bg) !important; color: var(--text) !important; }
            .q-header { border-bottom: 1px solid rgba(0,0,0,0.06); }
            .dark-mode .q-header { border-bottom: 1px solid rgba(255,255,255,0.03); }
            .q-page-container { padding: 0 !important; }
            body { margin: 0; overflow-x: hidden; }
            .rounded-borders { border-radius: 8px; }
            .compact-table .q-table__tbody td { padding-top: 6px; padding-bottom: 6px; }
            .header-bar { background: var(--accent); color: white; padding: 10px 16px; font-weight: 700; }
            .controls { padding: 12px 18px; display: flex; align-items: center; gap: 12px; background: transparent; }
            .controls { background: rgba(0,0,0,0.02); border-bottom: 1px solid rgba(15,23,42,0.04); }
            .dark-mode .controls { background: rgba(255,255,255,0.01); border-bottom: 1px solid rgba(255,255,255,0.03); }
            .table-card { width: calc(100% - 48px); max-width: none; margin: 12px 24px; background: var(--card); box-shadow: 0 1px 2px var(--card-elev); }
            .table-card .q-card__section { padding: 8px; }
            .compact-table table { table-layout: fixed; width: 100%; color: var(--text); }
            .compact-table thead th:nth-child(1), .compact-table tbody td:nth-child(1) { width: 8%; text-align: center; }
            .compact-table thead th:nth-child(2), .compact-table tbody td:nth-child(2) { width: 20%; }
            .compact-table thead th:nth-child(3), .compact-table tbody td:nth-child(3) { width: 20%; }
            .compact-table thead th:nth-child(4), .compact-table tbody td:nth-child(4) { width: 8%; text-align: center; }
            .compact-table thead th:nth-child(5), .compact-table tbody td:nth-child(5) { width: 44%; white-space: normal; overflow: hidden; text-overflow: ellipsis; }
            @media (min-width: 1200px) {
                .compact-table .q-table__tbody td { padding-top: 4px; padding-bottom: 4px; }
            }
            .q-table thead th { position: sticky; top: 0; background: var(--surface); z-index: 3; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
            .compact-table th, .compact-table td { color: var(--text) !important; background: transparent !important; font-weight: 500; opacity: 1 !important; }
            .compact-table .q-table__tbody td { padding-top: 10px; padding-bottom: 10px; border-bottom: 1px solid rgba(0,0,0,0.06); line-height: 1.25; }
            .dark-mode .compact-table .q-table__tbody td { border-bottom: 1px solid rgba(255,255,255,0.03); }
            .compact-table .q-table__tbody td:nth-child(5) { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
            .compact-table thead th { background: var(--surface); color: var(--text); font-weight: 700; }
            .dark-toggle { margin-left: 12px; }
            .table-card, .table-card .q-card__section, .q-card { background: var(--card) !important; color: var(--text) !important; }
            .q-card__section { padding: 12px !important; }
            .q-table, .q-table__container { background: transparent !important; }
            .compact-table th, .compact-table td { color: var(--text) !important; opacity: 1 !important; }
            .compact-table .q-table__tbody td { background: transparent !important; }
            .table-card { border: 1px solid rgba(15,23,42,0.06); }
            .dark-mode .table-card { border: 1px solid rgba(255,255,255,0.04); }
            .compact-table .q-table__tbody td { border-bottom: 1px solid rgba(0,0,0,0.04); }
            .dark-mode .compact-table .q-table__tbody td { border-bottom: 1px solid rgba(255,255,255,0.03); }
            /* Ensure form controls use theme colors (fixes invisible text in dark mode) */
            input, textarea, select, .q-field__native, .q-field__control input, .q-field__control textarea, .q-field__control select, .q-input__control input {
                color: var(--text) !important;
                background: transparent !important;
            }
            input::placeholder, textarea::placeholder {
                color: var(--muted) !important;
                opacity: 1 !important;
            }
            /* Properly styled empty-table area for compact tables: clear text, accent icon, surface inset */
            .compact-table .q-table__tbody td .q-table__empty__content,
            .compact-table .q-table__tbody td .q-empty,
            .compact-table .q-table__tbody td .q-table__bottom__empty {
                display: flex !important;
                align-items: center !important;
                gap: 12px !important;
                background: rgba(0,0,0,0.03) !important;
                padding: 10px 14px !important;
                border-radius: 6px !important;
                border: 1px solid rgba(0,0,0,0.04) !important;
            }
            .dark-mode .compact-table .q-table__tbody td .q-table__empty__content,
            .dark-mode .compact-table .q-table__tbody td .q-empty,
            .dark-mode .compact-table .q-table__tbody td .q-table__bottom__empty {
                background: rgba(255,255,255,0.02) !important;
                border: 1px solid rgba(255,255,255,0.03) !important;
            }
            .compact-table .q-table__tbody td .q-table__empty__text,
            .compact-table .q-table__tbody td .q-empty .q-table__empty__text {
                color: var(--text) !important;
                font-weight: 700 !important;
                opacity: 1 !important;
            }
            .compact-table .q-table__tbody td .q-table__empty__content .q-icon,
            .compact-table .q-table__tbody td .q-empty .q-icon {
                color: var(--accent) !important;
                fill: var(--accent) !important;
                opacity: 1 !important;
                margin-left: 6px !important;
            }
        </style>
    '''

