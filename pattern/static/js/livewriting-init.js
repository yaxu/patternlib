(function(){
    $(document).ready(function(){
        $('textarea.code-editor').each(function(idx, el){
            editor = CodeMirror.fromTextArea(el, {
                lineNumbers: true,
                mode: 'text/x-haskell',
		viewportMargin: Infinity
            });
            editor.livewriting = livewriting;
            editor.livewriting("create", "codemirror",{}, "");
        });
    });
})();

