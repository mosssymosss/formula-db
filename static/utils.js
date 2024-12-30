document.addEventListener('DOMContentLoaded', function() {
    $('#reset-database-button').click(function () {
        $('#reset-database-modal').modal('show');
    });

    $('#confirm-reset-database-button').click(function () {
        $.ajax({
            url: '/reset/',
            method: 'DELETE',
            success: function () {
                alert('Database has been reset successfully.');
                $('#reset-database-modal').modal('hide');
            },
            error: function (error) {
                console.error('Error resetting database:', error);
                alert('An error occurred while resetting the database.');
                $('#reset-database-modal').modal('hide');
            },
        });
    });
});