document.addEventListener('DOMContentLoaded', function() {
    // Menu buttons
    document.getElementById('circuits-menu').addEventListener('click', function() {
        document.getElementById('drivers-content').style.display = 'none';
        document.getElementById('circuits-content').style.display = 'block';
        document.getElementById('races-content').style.display = 'none';
        document.getElementById('response-content').innerHTML = '';
        
        document.querySelectorAll('.item').forEach(function(item) {
            item.classList.remove('active');
        });
        
        this.classList.add('active');
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
                num_of_circuits = data.num_circuits; 
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

        // Filter Circuits button
        $('#filter-circuits-button').click(function () {
            $('#filter-circuits-modal').modal('show');
        });


        $('#filter-circuits-search-button').click(function () {
            const location = $('#filter-location-input').val(); 
            const minlen = $('#filter-minlen-input').val();
            const maxlen = $('#filter-maxlen-input').val();
            const minlap = $('#filter-minlap-input').val();
            const maxlap = $('#filter-maxlap-input').val();

            if (!location && !minlen && !maxlen && !minlap && !maxlap) {
                alert('Please enter at least one correct filter value.');
                return;
            }

            function fetchFilteredCircuits(page = 1) {
                const params = new URLSearchParams();
                if (minlen) params.append('minlength', minlen);
                if (location) params.append('location', location);
                if (maxlen) params.append('maxlength', maxlen);
                if (minlap) params.append('minlaps', minlap);
                if (maxlap) params.append('maxlaps', maxlap);
                params.append('page', page);
                params.append('page_size', 100000);

                $.ajax({
                    url: `/circuits/filters/?${params.toString()}`, // Modify the query parameter as needed
                    method: 'GET',
                    success: function (data) {
                        renderFilteredCircuitsTable(data, page);
                    },
                    error: function (error) {
                        console.error('Error filtering circuits:', error);
                        $('#response-content').html('<p style="color: red;">An error occurred or no circuits matched the filter.</p>');
                        $('#filter-circuits-modal').modal('hide'); // Close the modal
                    },
                });
            }

            function renderFilteredCircuitsTable(circuits, page) {
                
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

                const totalPages = 1;
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
                    fetchFilteredCircuits(newPage);
                });
            }

            fetchFilteredCircuits(currentPage);
        });

        $('#sort-circuits-button').click(function () {
            $('#sort-circuits-modal').modal('show');
        });


        $('#sort-circuits-search-button').click(function () {
            const sortby = $('#sort-input').val(); 


            if (!sortby) {
                alert('Please enter at least one correct sort by value.');
                return;
            }

            function fetchSortedCircuits(page = 1) {
                const params = new URLSearchParams();
                if (sortby) params.append('sort_by', sortby);
                params.append('page', page);
                params.append('page_size', 10);

                $.ajax({
                    url: `/circuits/sorted/?${params.toString()}`, // Modify the query parameter as needed
                    method: 'GET',
                    success: function (data) {
                        renderSortedCircuitsTable(data, page);
                    },
                    error: function (error) {
                        console.error('Error filtering circuits:', error);
                        $('#response-content').html('<p style="color: red;">An error occurred or no circuits matched the filter.</p>');
                        $('#filter-circuits-modal').modal('hide'); // Close the modal
                    },
                });
            }

            

            function renderSortedCircuitsTable(circuits, page) {
                
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
                console.log(totalPages);
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
                    fetchSortedCircuits(newPage);
                });
            }

            fetchSortedCircuits(currentPage);
        });


        $('#search-circuits-button').click(function () {
            $('#search-circuits-modal').modal('show');
        });


        $('#search-circuits-search-button').click(function () {
            const search = $('#search-input').val(); 


            if (!search) {
                alert('Please enter at least one correct filter value.');
                return;
            }

            function fetchSearchCircuits(page = 1) {
                const params = new URLSearchParams();
                if (search) params.append('search', search);
                params.append('page', page);
                params.append('page_size', 100000000000);

                $.ajax({
                    url: `/circuits/search/?${params.toString()}`, // Modify the query parameter as needed
                    method: 'GET',
                    success: function (data) {
                        renderSearchCircuitsTable(data, page);
                    },
                    error: function (error) {
                        console.error('Error filtering circuits:', error);
                        $('#response-content').html('<p style="color: red;">An error occurred or no circuits matched the filter.</p>');
                        $('#filter-circuits-modal').modal('hide'); // Close the modal
                    },
                });
            }

            

            function renderSearchCircuitsTable(circuits, page) {
                
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

                const totalPages = 1;
                console.log(totalPages);
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
                    fetchSearchCircuits(newPage);
                });
            }

            fetchSearchCircuits(currentPage);
        });

        
    });
});
