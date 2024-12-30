document.addEventListener('DOMContentLoaded', function() {
    // Menu buttons
    document.getElementById('circuits-menu').addEventListener('click', function() {
        document.getElementById('drivers-content').style.display = 'none';
        document.getElementById('circuits-content').style.display = 'block';
        document.getElementById('races-content').style.display = 'none';
        document.getElementById('response-content').innerHTML = '';
    });

    // All drivers button
    $(document).ready(function () {
        let currentPage = 1;
        const pageSize = 10; 
        let num_of_circuits = 0;
        
        function fetchCircuits(page = 1) {
            const url = `/circuits/?page=${page}&page_size=${pageSize}`;
            $.ajax({
                url: url,
                method: 'GET',
                success: function (data) {
                    renderCircuitsTable(data, page);
                },
                error: function (error) {
                    console.error('Error fetching circuits:', error);
                    $('#response-content').html('<p style="color: red;">An error occurred while fetching circuits.</p>');
                },
            });
        }

        function fetchNumberOfCircuits() {
            return $.ajax({
                url: '/circuits/circuit_count/',
                method: 'GET',
            }).then(function (data) {
                num_of_circuits = data.num_drivers; 
                return num_of_circuits; 
            }).catch(function (error) {
                console.error('Error fetching number of drivers:', error);
                throw error; 
            });
        }

        fetchNumberOfCircuits().then(function(num_of_circuits) {
            console.log('Number of circuits:', num_of_circuits);
        });

        function renderCircuitsTable(circuits, page) {
            let tableHtml = `
                <table class="ui celled inverted table">
                    <thead>
                        <tr>
                            <th>Circuit ID</th>
                            <th>Name</th>
                            <th>Location</th>
                            <th>Length (km)</th>
                            <th>Laps</th>
                            <th>Lap Record</th>
                            <th>Description</th>
                            <th>Created By</th>
                            <th>Created At</th>
                            <th>Active</th>
                            <th>Events Hosted</th>
                            <th>Average Attendance</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            circuits.forEach(circuit => {
                tableHtml += `
                    <tr>
                        <td data-label="Circuit ID">${circuit.circuit_id}</td>
                        <td data-label="Name">${circuit.name}</td>
                        <td data-label="Location">${circuit.location}</td>
                        <td data-label="Length (km)">${circuit.length_km}</td>
                        <td data-label="Laps">${circuit.laps}</td>
                        <td data-label="Lap Record">${circuit.lap_record}</td>
                        <td data-label="Description">${circuit.info.description}</td>
                        <td data-label="Created By">${circuit.info.created_by}</td>
                        <td data-label="Created At">${circuit.info.created_at}</td>
                        <td data-label="Active">${circuit.info.is_active}</td>
                        <td data-label="Events Hosted">${circuit.info.events_hosted}</td>
                        <td data-label="Average Attendance">${circuit.info.average_attendance}</td>
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

            const totalPages = Math.ceil(num_of_circuits / pageSize);
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
                fetchCircuits(newPage);
            });
        }

        $('#all-circuits-button').click(function () {
            fetchCircuits(currentPage);
        });

        // Circuit by ID button
        $('#circuit-by-id-button').click(function () {
            $('#circuit-id-modal').modal('show');
        });

        $('#search-circuit-button').click(function () {
            const circuitId = $('#circuit-id-input').val(); 

            if (!circuitId) {
                alert('Please enter a valid Circuit ID');
                return;
            }

            $.ajax({
                url: `/circuits/${circuitId}`,
                method: 'GET',
                success: function (circuit) {
                    const circuitHtml = `
                        <table class="ui celled inverted table">
                            <thead>
                                <tr>
                                    <th>Circuit ID</th>
                                    <th>Name</th>
                                    <th>Location</th>
                                    <th>Length (km)</th>
                                    <th>Laps</th>
                                    <th>Lap Record</th>
                                    <th>Description</th>
                                    <th>Created By</th>
                                    <th>Created At</th>
                                    <th>Active</th>
                                    <th>Events Hosted</th>
                                    <th>Average Attendance</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td data-label="Circuit ID">${circuit.circuit_id}</td>
                                    <td data-label="Name">${circuit.name}</td>
                                    <td data-label="Location">${circuit.location}</td>
                                    <td data-label="Length (km)">${circuit.length_km}</td>
                                    <td data-label="Laps">${circuit.laps}</td>
                                    <td data-label="Lap Record">${circuit.lap_record}</td>
                                    <td data-label="Description">${circuit.info.description}</td>
                                    <td data-label="Created By">${circuit.info.created_by}</td>
                                    <td data-label="Created At">${circuit.info.created_at}</td>
                                    <td data-label="Active">${circuit.info.is_active}</td>
                                    <td data-label="Events Hosted">${circuit.info.events_hosted}</td>
                                    <td data-label="Average Attendance">${circuit.info.average_attendance}</td>
                                </tr>
                            </tbody>
                        </table>
                    `;

                    $('#response-content').html(circuitHtml); 
                    $('#circuit-id-modal').modal('hide'); 
                },
                error: function (error) {
                    console.error('Error fetching circuit:', error);
                    $('#response-content').html('<p style="color: red;">Circuit not found or an error occurred.</p>');
                    $('#Circuit-id-modal').modal('hide'); 
                },
            });
        });

    });
});
