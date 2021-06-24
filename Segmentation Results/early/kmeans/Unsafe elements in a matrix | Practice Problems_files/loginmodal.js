(function(global){
    global.showLoginModal = function() {
        jQuery('#login-modal').show();
        jQuery('#login-modal').modal({
            onClose(dialog) {
            dialog.data.fadeOut(300);
            dialog.container.fadeOut(300, function() {
                dialog.overlay.hide();
                jQuery.modal.close();
                jQuery('.modal-window').hide();
            });
            },
            onOpen(dialog) {
            dialog.overlay.fadeIn(300);
            dialog.data.show();
            dialog.container.fadeIn(300);
            },
        });
        return false;
    }
})(window);