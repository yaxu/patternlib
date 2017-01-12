(function(){
    var $ = django.jQuery;
    $(document).ready(function(){
        $('textarea.code-editor').each(function(idx, el){
            CodeMirror.fromTextArea(el, {
                lineNumbers: true,
                mode: 'text/x-haskell'
            });
        });
    });
})();
