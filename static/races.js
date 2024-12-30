document.addEventListener('DOMContentLoaded', function() {
    // Menu buttons

    document.getElementById('races-menu').addEventListener('click', function() {
        document.getElementById('drivers-content').style.display = 'none';
        document.getElementById('circuits-content').style.display = 'none';
        document.getElementById('races-content').style.display = 'block';
        document.getElementById('response-content').innerHTML = '';
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

    });
});