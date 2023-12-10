(
    echo '<html><head><style>.wall, .empty { font-family: monospace; } .wall { color: red; } </style></head><body>';
    ./solv-2-draw.py | sed -r -e '1d' -e 's#([^.])#<span class="wall">\1</span>#g' -e 's#[.]#<span class="empty">.</span>#g';
    echo '</body</html>'
) > solv-2.html
