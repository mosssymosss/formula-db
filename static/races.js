document.addEventListener('DOMContentLoaded', function() {
    // Menu buttons

    document.getElementById('races-menu').addEventListener('click', function() {
        document.getElementById('drivers-content').style.display = 'none';
        document.getElementById('circuits-content').style.display = 'none';
        document.getElementById('races-content').style.display = 'block';
        document.getElementById('response-content').innerHTML = '';
    

        document.querySelectorAll('.item').forEach(function(item) {
            item.classList.remove('active');
        });

        this.classList.add('active');
    });
    // All races button
    $(document).ready(function () {
        let currentPage = 1;
        const pageSize = 10; 
        let num_of_races = 0;
        
        function fetchRaces(page = 1) {
            const url = `/races/?page=${page}&page_size=${pageSize}`;
            $.ajax({
                url: url,
                method: 'GET',
                success: function (data) {
                    renderRacesTable(data, page);
                },
                error: function (error) {
                    console.error('Error fetching races:', error);
                    $('#response-content').html('<p style="color: red;">An error occurred while fetching races.</p>');
                },
            });
        }

        function fetchNumberOfRaces() {
            return $.ajax({
                url: '/races/race_count/',
                method: 'GET',
            }).then(function (data) {
                num_of_races = data.num_races; 
                return num_of_races; 
            }).catch(function (error) {
                console.error('Error fetching number of races:', error);
                throw error; 
            });
        }

        fetchNumberOfRaces().then(function(num_of_races) {
            console.log('Number of races:', num_of_races);
        });

        function renderRacesTable(races, page) {
            let tableHtml = `
                <table class="ui celled inverted table">
                    <thead>
                        <tr>
                            <th>Driver ID</th>
                            <th>Circuit ID</th>
                            <th>Race Date</th>
                            <th>Place</th>
                            <th>Points</th>
                            <th>Fastest Lap</th>
                            <th>Start Place</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            races.forEach(race => {
                tableHtml += `
                    <tr>
                        <td data-label="Race ID">${race.driver_id}</td>
                        <td data-label="Circuit ID">${race.circuit_id}</td>
                        <td data-label="Race Date">${race.race_date}</td>
                        <td data-label="Place">${race.place}</td>
                        <td data-label="Points">${race.points}</td>
                        <td data-label="Fastest Lap">${race.is_fastest_lap}</td>
                        <td data-label="Start Place">${race.start_place}</td>
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

            const totalPages = Math.ceil(num_of_races / pageSize);
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
                fetchRaces(newPage);
            });
        }

        $('#all-races-button').click(function () {
            fetchRaces(currentPage);
        });

        // Race by ID button
        $('#race-by-id-button').click(function () {
            $('#race-id-modal').modal('show');
        });

        $('#search-race-button').click(function () {
            const driverId = $('#race-driver-id-input').val(); 
            const circuitId = $('#race-circuit-id-input').val();
            const raceDate = $('#race-date-input').val();

            if (!driverId && !circuitId && !raceDate) {
                alert('Please enter at least one search parameter');
                return;
            }

            const params = new URLSearchParams();
            if (driverId) params.append('driver_id', driverId);
            if (circuitId) params.append('circuit_id', circuitId);
            if (raceDate) params.append('race_date', raceDate);

            $.ajax({
                url: `/races/${driverId}/${circuitId}/${raceDate}`,
                method: 'GET',
                success: function (race) {
                    let raceHtml = `
                        <table class="ui celled inverted table">
                            <thead>
                                <tr>
                                    <th>Driver ID</th>
                                    <th>Circuit ID</th>
                                    <th>Race Date</th>
                                    <th>Place</th>
                                    <th>Points</th>
                                    <th>Fastest Lap</th>
                                    <th>Start Place</th>
                                </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td data-label="Driver ID">${race.driver_id}</td>
                                <td data-label="Circuit ID">${race.circuit_id}</td>
                                <td data-label="Race Date">${race.race_date}</td>
                                <td data-label="Place">${race.place}</td>
                                <td data-label="Points">${race.points}</td>
                                <td data-label="Fastest Lap">${race.is_fastest_lap}</td>
                                <td data-label="Start Place">${race.start_place}</td>
                            </tr>
                            </tbody>
                        </table>
                    `;

                    $('#response-content').html(raceHtml); 
                    $('#race-id-modal').modal('hide'); 
                },
                error: function (error) {
                    console.error('Error fetching races:', error);
                    $('#response-content').html('<p style="color: red;">Races not found or an error occurred.</p>');
                    $('#race-id-modal').modal('hide'); 
                },
            });
        });


        // Filter Races button
        $('#filter-races-button').click(function () {
            $('#filter-races-modal').modal('show');
        });


        $('#filter-races-search-button').click(function () {
            const driverID = $('#filter-races-driver-id-input').val(); 
            const circuitID = $('#filter-races-circuit-id-input').val();
            const startDate = $('#filter-start-date-input').val();
            const endDate = $('#filter-end-date-input').val();
            const minPoints = $('#filter-min-points-input').val();
            const maxPoints = $('#filter-max-points-input').val();
            const fastestLap = $('#filter-fastest-lap-input').val();


            if (!driverID && !circuitID && !startDate && !endDate && !minPoints && !maxPoints && !fastestLap) {
                alert('Please enter at least one correct filter value.');
                return;
            }

            function fetchFilteredRaces(page = 1) {
                const params = new URLSearchParams();
                if (circuitID) params.append('minlength', circuitID);
                if (driverID) params.append('location', driverID);
                if (startDate) params.append('maxlength', startDate);
                if (endDate) params.append('minlaps', endDate);
                if (minPoints) params.append('maxlaps', minPoints);
                if (maxPoints) params.append('minlaps', maxPoints);
                if (fastestLap) params.append('fastest_lap', fastestLap);
                params.append('page', page);
                params.append('page_size', 100000);

                $.ajax({
                    url: `/races/filters/?${params.toString()}`, // Modify the query parameter as needed
                    method: 'GET',
                    success: function (data) {
                        renderFilteredRacesTable(data, page);
                    },
                    error: function (error) {
                        console.error('Error filtering races:', error);
                        $('#response-content').html('<p style="color: red;">An error occurred or no races matched the filter.</p>');
                        $('#filter-races-modal').modal('hide'); // Close the modal
                    },
                });
            }

            function renderFilteredRacesTable(races, page) {
                
                let tableHtml = `
                    <table class="ui celled inverted table">
                    <thead>
                        <tr>
                            <th>Driver ID</th>
                            <th>Circuit ID</th>
                            <th>Race Date</th>
                            <th>Place</th>
                            <th>Points</th>
                            <th>Fastest Lap</th>
                            <th>Start Place</th>
                        </tr>
                    </thead>
                    <tbody>
                `;

                races.forEach(race => {
                    tableHtml += `
                                <tr>
                                    <td data-label="Race ID">${race.driver_id}</td>
                                    <td data-label="Circuit ID">${race.circuit_id}</td>
                                    <td data-label="Race Date">${race.race_date}</td>
                                    <td data-label="Place">${race.place}</td>
                                    <td data-label="Points">${race.points}</td>
                                    <td data-label="Fastest Lap">${race.is_fastest_lap}</td>
                                    <td data-label="Start Place">${race.start_place}</td>
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
                    fetchFilteredRaces(newPage);
                });
            }

            fetchFilteredRaces(currentPage);
        });

        $('#delete-race-button').click(function () {
            $('#race-id-modal-2').modal('show');
        });
        
        $('#search-race-button').click(function () {
            const driverId = $('#race-driver-id-input-2').val(); 
            const circuitId = $('#race-circuit-id-input-2').val();
            const raceDate = $('#race-date-input-2').val(); 
        
            if (!driverId && !circuitId && !raceDate) {
                alert('Please enter valid values');
                return;
            }
        
            $.ajax({
                url: `/races/${driverId}/${circuitId}/${raceDate}`,
                method: 'DELETE',
                success: function (response) {
                    $('#response-content').html('Race has been deleted successfully.');
                    $('#race-id-modal-2').modal('hide');
                },
                error: function (error) {
                    alert('An error occurred while deleting.');
                    $('#race-id-modal-2').modal('hide');
                },
            });
        });


        $('#create-race-button').click(function () {
            $('#create-races-modal').modal('show');
        });
    
        // Handle the Create Race confirmation button
        $('#create-races-search-button').click(function () {
            const driverId = $('#create-driver-id-input-2').val();
            const circuitId = $('#create-circuit-id-input-2').val();
            const raceDate = $('#create-race-date-input').val();
            const place = $('#create-place-input').val();
            const points = $('#create-points-input').val();
            const isFastestLap = $('#create-is-fastest-lap-input').val();
            const startPlace = $('#create-start-place-input').val();
    
            // Log the data for debugging purposes
            console.log({
                driverId,
                circuitId,
                raceDate,
                place,
                points,
                isFastestLap,
                startPlace,
            });

            // Validate required fields
            if (
                !driverId ||
                !circuitId ||
                !raceDate ||
                !place ||
                !points ||
                !isFastestLap ||
                !startPlace
            ) {
                alert('Please enter all required fields.');
                return;
            }
    
            // Prepare race data for the POST request
            const raceData = {
                driver_id: parseInt(driverId),
                circuit_id: parseInt(circuitId),
                race_date: raceDate,
                place: parseInt(place),
                points: parseInt(points),
                is_fastest_lap: isFastestLap.toLowerCase() === 'true',
                start_place: parseInt(startPlace),
            };
    
            // Send POST request to create a new race
            $.ajax({
                url: `/races/`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(raceData),
                success: function (response) {
                    $('#response-content').html('<p style="color: green;">Race has been created successfully.</p>');
                    $('#create-races-modal').modal('hide');
                },
                error: function (error) {
                    console.error('Error creating race:', error);
                    alert('An error occurred while creating the race.');
                    $('#create-races-modal').modal('hide');
                },
            });
        });
    
        // Handle the cancel button to close the modal
        $('.ui.red.basic.cancel.button').click(function () {
            $('#create-races-modal').modal('hide');
        });


        $('#update-race-button').click(function () {
            $('#update-race-modal').modal('show');
        });
    
        // Handle the Update Race confirmation button
        $('#update-race-confirm-button').click(function () {
            // Collect the race identifiers (driver_id, circuit_id, race_date) from hidden inputs or external selection
            const driverId = $('#update-race-driver-id-input').val(); // Ensure this field exists
            const circuitId = $('#update-race-circuit-id-input').val(); // Ensure this field exists
            const raceDate = $('#update-race-date-input').val(); // Ensure this field exists
    
            // Collect the updated race details
            const place = $('#update-race-place-input').val();
            const points = $('#update-race-points-input').val();
            const isFastestLap = $('#update-race-is-fastest-lap-input').val();
    
            // Log the data for debugging purposes
            console.log('Updating Race:', {
                driverId,
                circuitId,
                raceDate,
                place,
                points,
                isFastestLap,
            });
    
            // Validate the required fields
            if (!driverId || !circuitId || !raceDate) {
                alert('Driver ID, Circuit ID, and Race Date are required to update a race.');
                return;
            }
    
            // Prepare the update data (only include fields that are not empty)
            const updateData = {};
            if (place) updateData.place = parseInt(place);
            if (points) updateData.points = parseInt(points);
            if (isFastestLap) updateData.is_fastest_lap = isFastestLap.toLowerCase() === 'true';
    
            // Check if any data is provided
            if (Object.keys(updateData).length === 0) {
                alert('Please provide at least one field to update.');
                return;
            }
    
            // Send the PUT request to update the race
            $.ajax({
                url: `/races/?driver_id=${driverId}&circuit_id=${circuitId}&race_date=${raceDate}`,
                method: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(updateData),
                success: function (response) {
                    $('#response-content').html('<p style="color: green;">Race has been updated successfully.</p>');
                    $('#update-race-modal').modal('hide');
                },
                error: function (error) {
                    console.error('Error updating race:', error);
                    alert('An error occurred while updating the race.');
                    $('#update-race-modal').modal('hide');
                },
            });
        });
    
        // Handle the cancel button to close the modal
        $('.ui.red.basic.cancel.button').click(function () {
            $('#update-race-modal').modal('hide');
        });
    });
});