(function () {
    $('.mdeditor-preview-area').each(function () {
        var area_id = $(this).attr('id');
        var config = JSON.parse($(this).find('textarea').attr('mdeditor-preview-config'));
        editormd.markdownToHTML(area_id,config);
    });
})();