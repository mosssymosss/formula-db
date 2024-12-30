document.addEventListener('DOMContentLoaded', function() {
    // Menu buttons
    document.getElementById('drivers-menu').addEventListener('click', function() {
        document.getElementById('drivers-content').style.display = 'block';
        document.getElementById('circuits-content').style.display = 'none';
        document.getElementById('races-content').style.display = 'none';
        document.getElementById('response-content').innerHTML = '';
    });


    // All drivers button
    $(document).ready(function () {
        let currentPage = 1;
        const pageSize = 10; 
        let num_of_drivers = 0;
        
        function fetchDrivers(page = 1) {
            const url = `/drivers/?page=${page}&page_size=${pageSize}`;
            $.ajax({
                url: url,
                method: 'GET',
                success: function (data) {
                    renderDriversTable(data, page);
                },
                error: function (error) {
                    console.error('Error fetching drivers:', error);
                    $('#response-content').html('<p style="color: red;">An error occurred while fetching drivers.</p>');
                },
            });
        }

        function fetchNumberOfDrivers() {
            return $.ajax({
                url: '/drivers/driver_count/',
                method: 'GET',
            }).then(function (data) {
                num_of_drivers = data.num_drivers; 
                return num_of_drivers; 
            }).catch(function (error) {
                console.error('Error fetching number of drivers:', error);
                throw error; 
            });
        }

        fetchNumberOfDrivers().then(function(num_of_drivers) {
            console.log('Number of drivers:', num_of_drivers);
        });

        function renderDriversTable(drivers, page) {
            let tableHtml = `
                <table class="ui celled inverted table">
                    <thead>
                        <tr>
                            <th>Driver ID</th>
                            <th>Number</th>
                            <th>Name</th>
                            <th>Nationality</th>
                            <th>Team</th>
                            <th>Date of Birth</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            drivers.forEach(driver => {
                tableHtml += `
                    <tr>
                        <td data-label="Driver ID">${driver.driver_id}</td>
                        <td data-label="Number">${driver.number}</td>
                        <td data-label="Name">${driver.name}</td>
                        <td data-label="Nationality">${driver.nationality}</td>
                        <td data-label="Team">${driver.team}</td>
                        <td data-label="Date of Birth">${driver.dob}</td>
                    </tr>
                `;
            });

            tableHtml += `
                    </tbody>
                </table>
            `;

            let paginationHtml = `
                <div class="ui pagination inverted menu">
                    <a class="item" data-page="${page - 1}" ${page === 1 ? 'disabled' : ''}>Previous</a>
            `;

            const totalPages = Math.ceil(num_of_drivers / pageSize);
            const startPage = Math.max(1, page - 2);
            const endPage = Math.min(totalPages, page + 2);

            for (let i = startPage; i <= endPage; i++) {
                paginationHtml += `
                    <a class="item ${i === page ? 'active' : ''}" data-page="${i}">${i}</a>
                `;
            }

            paginationHtml += `
                    <a class="item" data-page="${page + 1}" ${page === totalPages ? 'disabled' : ''}>Next</a>
                </div>
            `;

            $('#response-content').html(tableHtml + paginationHtml);

            $('.ui.pagination.menu .item').not('[disabled]').click(function () {
                const newPage = $(this).data('page');
                fetchDrivers(newPage);
            });
        }

        $('#all-drivers-button').click(function () {
            fetchDrivers(currentPage);
        });

        // Driver by ID button
        $('#driver-by-id-button').click(function () {
            $('#driver-id-modal').modal('show');
        });

        $('#search-driver-button').click(function () {
            const driverId = $('#driver-id-input').val(); 

            if (!driverId) {
                alert('Please enter a valid Driver ID');
                return;
            }

            $.ajax({
                url: `/drivers/${driverId}`,
                method: 'GET',
                success: function (driver) {
                    const driverHtml = `
                        <table class="ui celled inverted table">
                            <thead>
                                <tr>
                                    <th>Driver ID</th>
                                    <th>Number</th>
                                    <th>Name</th>
                                    <th>Nationality</th>
                                    <th>Team</th>
                                    <th>Date of Birth</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>${driver.driver_id}</td>
                                    <td>${driver.number}</td>
                                    <td>${driver.name}</td>
                                    <td>${driver.nationality}</td>
                                    <td>${driver.team}</td>
                                    <td>${driver.dob}</td>
                                </tr>
                            </tbody>
                        </table>
                    `;

                    $('#response-content').html(driverHtml); 
                    $('#driver-id-modal').modal('hide'); 
                },
                error: function (error) {
                    console.error('Error fetching driver:', error);
                    $('#response-content').html('<p style="color: red;">Driver not found or an error occurred.</p>');
                    $('#driver-id-modal').modal('hide'); 
                },
            });
        });

    });
});
