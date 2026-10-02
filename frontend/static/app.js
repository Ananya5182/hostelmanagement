/**
 * CampusStay - Enterprise Hostel Management System
 * Frontend Client-Side Application Logic (Vanilla JavaScript)
 * Author: Janvi Chattani (@janvichattani21-glitch)
 * Issue: HMS-2 (Reactive Allocation Form & Dynamic Dropdown)
 */

document.addEventListener('DOMContentLoaded', () => {
    // State Store
    const state = {
        rooms: [],
        students: [],
        stats: null,
        isHealthUp: false,
    };

    // DOM Elements
    const healthBadge = document.getElementById('system-health-badge');
    const healthStatusText = document.getElementById('health-status-text');
    const clockEl = document.getElementById('current-clock');
    const btnRefresh = document.getElementById('btn-refresh');

    // KPI Elements
    const kpiTotalRooms = document.getElementById('kpi-total-rooms');
    const kpiOccupiedBeds = document.getElementById('kpi-occupied-beds');
    const kpiCapacitySubtext = document.getElementById('kpi-capacity-subtext');
    const kpiAvailableBeds = document.getElementById('kpi-available-beds');
    const kpiOccupancyRate = document.getElementById('kpi-occupancy-rate');
    const kpiProgressBar = document.getElementById('kpi-progress-bar');

    // Form Elements
    const form = document.getElementById('student-allocation-form');
    const roomSelect = document.getElementById('room-select');
    const availableRoomsCount = document.getElementById('available-rooms-count');
    const btnSubmit = document.getElementById('btn-submit-allocation');
    const btnSpinner = btnSubmit.querySelector('.btn-spinner');
    const btnText = btnSubmit.querySelector('.btn-text');
    const checkinInput = document.getElementById('student-checkin');

    // Table Elements
    const roomsTableBody = document.getElementById('rooms-table-body');
    const roomsCounterBadge = document.getElementById('rooms-counter-badge');
    const searchRoomsInput = document.getElementById('search-rooms');
    const filterRoomStatus = document.getElementById('filter-room-status');

    const studentsTableBody = document.getElementById('students-table-body');
    const studentsCounterBadge = document.getElementById('students-counter-badge');
    const searchStudentsInput = document.getElementById('search-students');

    const toastContainer = document.getElementById('toast-container');

    // Set default checkin date to today
    if (checkinInput) {
        checkinInput.value = new Date().toISOString().split('T')[0];
    }

    // ==========================================
    // Clock & Health Check
    // ==========================================
    function updateClock() {
        const now = new Date();
        clockEl.textContent = now.toLocaleTimeString('en-US', { hour12: false });
    }
    setInterval(updateClock, 1000);
    updateClock();

    async function checkHealth() {
        try {
            const res = await fetch('/health');
            const data = await res.json();
            if (res.ok && data.status === 'UP') {
                state.isHealthUp = true;
                healthBadge.className = 'health-badge status-up';
                healthStatusText.textContent = 'Backend: Connected';
            } else {
                state.isHealthUp = false;
                healthBadge.className = 'health-badge status-down';
                healthStatusText.textContent = 'Backend: Degraded';
            }
        } catch (err) {
            state.isHealthUp = false;
            healthBadge.className = 'health-badge status-down';
            healthStatusText.textContent = 'Backend: Offline';
        }
    }

    // ==========================================
    // Data Fetching
    // ==========================================
    async function fetchAllData() {
        await Promise.all([
            checkHealth(),
            fetchRooms(),
            fetchStudents(),
            fetchStats()
        ]);
    }

    async function fetchRooms() {
        try {
            const res = await fetch('/api/rooms');
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            state.rooms = await res.json();
            renderRoomsTable();
            populateRoomDropdown();
        } catch (err) {
            console.error('Error fetching rooms:', err);
            roomsTableBody.innerHTML = `<tr><td colspan="7" class="table-placeholder">Failed to load rooms. Please check backend connection.</td></tr>`;
        }
    }

    async function fetchStudents() {
        try {
            const res = await fetch('/api/students');
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            state.students = await res.json();
            renderStudentsTable();
        } catch (err) {
            console.error('Error fetching students:', err);
            studentsTableBody.innerHTML = `<tr><td colspan="6" class="table-placeholder">Failed to load student registry.</td></tr>`;
        }
    }

    async function fetchStats() {
        try {
            const res = await fetch('/api/stats');
            if (res.ok) {
                state.stats = await res.json();
                renderKPIs(state.stats);
            } else {
                computeFallbackKPIs();
            }
        } catch (err) {
            computeFallbackKPIs();
        }
    }

    function computeFallbackKPIs() {
        const totalRooms = state.rooms.length;
        const totalCapacity = state.rooms.reduce((acc, r) => acc + (r.capacity || 0), 0);
        const totalOccupied = state.rooms.reduce((acc, r) => acc + (r.occupied || 0), 0);
        const availableBeds = Math.max(0, totalCapacity - totalOccupied);
        const occupancyRate = totalCapacity > 0 ? ((totalOccupied / totalCapacity) * 100).toFixed(1) : 0;

        renderKPIs({
            total_rooms: totalRooms,
            total_capacity: totalCapacity,
            total_occupied: totalOccupied,
            available_beds: availableBeds,
            occupancy_rate: occupancyRate
        });
    }

    function renderKPIs(stats) {
        kpiTotalRooms.textContent = stats.total_rooms;
        kpiOccupiedBeds.textContent = stats.total_occupied;
        kpiCapacitySubtext.textContent = `out of ${stats.total_capacity} total beds`;
        kpiAvailableBeds.textContent = stats.available_beds;
        kpiOccupancyRate.textContent = `${stats.occupancy_rate}%`;
        kpiProgressBar.style.width = `${Math.min(100, Math.max(0, stats.occupancy_rate))}%`;
    }

    // ==========================================
    // Populate Dynamic Room Dropdown
    // ==========================================
    function populateRoomDropdown() {
        const availableRooms = state.rooms.filter(r => 
            (r.status === 'AVAILABLE' || r.status === 'OPEN') && 
            (r.occupied < r.capacity)
        );

        availableRoomsCount.textContent = `${availableRooms.length} Available`;

        // Preserve current selection if valid
        const previousValue = roomSelect.value;
        roomSelect.innerHTML = '<option value="" disabled selected>Select an available room...</option>';

        if (availableRooms.length === 0) {
            const opt = document.createElement('option');
            opt.disabled = true;
            opt.textContent = 'No available rooms currently';
            roomSelect.appendChild(opt);
            return;
        }

        availableRooms.forEach(room => {
            const vacantBeds = room.capacity - room.occupied;
            const option = document.createElement('option');
            option.value = room.id;
            option.textContent = `${room.room_number} (${room.block_name || 'Standard'} - ${formatRoomType(room.room_type)}) • ${vacantBeds} bed${vacantBeds > 1 ? 's' : ''} free`;
            if (String(room.id) === previousValue) {
                option.selected = true;
            }
            roomSelect.appendChild(option);
        });
    }

    // ==========================================
    // Render Rooms Table
    // ==========================================
    function renderRoomsTable() {
        const query = (searchRoomsInput.value || '').trim().toLowerCase();
        const statusFilter = filterRoomStatus.value;

        const filtered = state.rooms.filter(room => {
            const matchQuery = (
                (room.room_number && room.room_number.toLowerCase().includes(query)) ||
                (room.block_name && room.block_name.toLowerCase().includes(query)) ||
                (room.room_type && room.room_type.toLowerCase().includes(query))
            );
            const matchStatus = (statusFilter === 'ALL' || room.status === statusFilter);
            return matchQuery && matchStatus;
        });

        roomsCounterBadge.textContent = `${filtered.length} of ${state.rooms.length} Rooms`;

        if (filtered.length === 0) {
            roomsTableBody.innerHTML = `<tr><td colspan="7" class="table-placeholder">No matching rooms found.</td></tr>`;
            return;
        }

        roomsTableBody.innerHTML = filtered.map(room => {
            const occupied = room.occupied || 0;
            const capacity = room.capacity || 1;
            const percent = Math.min(100, Math.round((occupied / capacity) * 100));
            const statusClass = getStatusClass(room.status);
            const feeFormatted = room.monthly_fee ? `₹${Number(room.monthly_fee).toLocaleString('en-IN')}` : 'Included';

            return `
                <tr>
                    <td><strong>${escapeHtml(room.room_number)}</strong></td>
                    <td>${escapeHtml(room.block_name || 'Block A')}</td>
                    <td>${formatRoomType(room.room_type)}</td>
                    <td>${capacity} Beds</td>
                    <td>
                        <div class="occupancy-cell">
                            <span>${occupied}/${capacity}</span>
                            <div class="mini-bar-bg" title="${percent}% Occupied">
                                <div class="mini-bar-fill ${occupied >= capacity ? 'fill-full' : ''}" style="width: ${percent}%;"></div>
                            </div>
                        </div>
                    </td>
                    <td>${feeFormatted}</td>
                    <td><span class="status-pill ${statusClass}">${escapeHtml(room.status)}</span></td>
                </tr>
            `;
        }).join('');
    }

    // ==========================================
    // Render Students Table
    // ==========================================
    function renderStudentsTable() {
        const query = (searchStudentsInput.value || '').trim().toLowerCase();

        const filtered = state.students.filter(student => {
            const roomNumber = student.rooms ? student.rooms.room_number : '';
            return (
                (student.name && student.name.toLowerCase().includes(query)) ||
                (student.email && student.email.toLowerCase().includes(query)) ||
                (roomNumber && roomNumber.toLowerCase().includes(query))
            );
        });

        studentsCounterBadge.textContent = `${filtered.length} Students`;

        if (filtered.length === 0) {
            studentsTableBody.innerHTML = `<tr><td colspan="6" class="table-placeholder">No allocated students found matching criteria.</td></tr>`;
            return;
        }

        studentsTableBody.innerHTML = filtered.map(student => {
            const initials = getInitials(student.name);
            const roomObj = student.rooms;
            const roomNumber = roomObj ? roomObj.room_number : `Room #${student.room_id}`;
            const blockName = roomObj && roomObj.block_name ? ` (${roomObj.block_name})` : '';
            const roomType = roomObj ? formatRoomType(roomObj.room_type) : 'Standard';
            const checkin = student.check_in_date ? student.check_in_date : 'N/A';

            return `
                <tr>
                    <td>
                        <div class="student-meta-cell">
                            <div class="student-avatar">${escapeHtml(initials)}</div>
                            <strong>${escapeHtml(student.name)}</strong>
                        </div>
                    </td>
                    <td>
                        <div class="contact-cell">
                            <span class="contact-email">${escapeHtml(student.email)}</span>
                            <span class="contact-phone">${escapeHtml(student.phone)}</span>
                        </div>
                    </td>
                    <td>
                        <span class="contact-phone">${escapeHtml(student.emergency_contact || 'None')}</span>
                    </td>
                    <td>
                        <span class="room-badge">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M3 21h18M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16"></path>
                            </svg>
                            ${escapeHtml(roomNumber)}${escapeHtml(blockName)}
                        </span>
                    </td>
                    <td>${escapeHtml(roomType)}</td>
                    <td>${escapeHtml(checkin)}</td>
                </tr>
            `;
        }).join('');
    }

    // ==========================================
    // Handle Student Allocation Form Submit
    // ==========================================
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('student-name').value.trim();
        const email = document.getElementById('student-email').value.trim();
        const phone = document.getElementById('student-phone').value.trim();
        const emergency_contact = document.getElementById('student-emergency').value.trim() || null;
        const check_in_date = document.getElementById('student-checkin').value || null;
        const room_id = parseInt(roomSelect.value, 10);

        if (!room_id) {
            showToast('Please select a valid room.', 'error');
            return;
        }

        const payload = {
            name,
            email,
            phone,
            emergency_contact,
            check_in_date,
            room_id
        };

        // Loading state
        setFormLoading(true);

        try {
            const res = await fetch('/api/students', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Allocation failed');
            }

            showToast(`Success! Room allocated to ${name}.`, 'success');
            form.reset();
            if (checkinInput) {
                checkinInput.value = new Date().toISOString().split('T')[0];
            }

            // Immediately refresh all data
            await fetchAllData();
        } catch (err) {
            console.error('Allocation error:', err);
            showToast(err.message, 'error');
        } finally {
            setFormLoading(false);
        }
    });

    function setFormLoading(isLoading) {
        btnSubmit.disabled = isLoading;
        if (isLoading) {
            btnSpinner.classList.remove('hidden');
            btnText.textContent = 'Allocating...';
        } else {
            btnSpinner.classList.add('hidden');
            btnText.textContent = 'Confirm Allocation';
        }
    }

    // ==========================================
    // Toast Notification Utility
    // ==========================================
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        const iconSvg = type === 'success' 
            ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>`
            : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;

        toast.innerHTML = `
            ${iconSvg}
            <span>${escapeHtml(message)}</span>
        `;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            setTimeout(() => toast.remove(), 300);
        }, 4500);
    }

    // ==========================================
    // Filter Event Listeners
    // ==========================================
    searchRoomsInput.addEventListener('input', renderRoomsTable);
    filterRoomStatus.addEventListener('change', renderRoomsTable);
    searchStudentsInput.addEventListener('input', renderStudentsTable);
    btnRefresh.addEventListener('click', () => {
        btnRefresh.style.transform = 'rotate(180deg)';
        fetchAllData().then(() => {
            setTimeout(() => btnRefresh.style.transform = '', 300);
            showToast('Hostel records refreshed', 'info');
        });
    });

    // ==========================================
    // Helper Formatting Functions
    // ==========================================
    function getStatusClass(status) {
        switch ((status || '').toUpperCase()) {
            case 'AVAILABLE':
            case 'OPEN':
                return 'status-available';
            case 'FULL':
            case 'OCCUPIED':
                return 'status-full';
            case 'MAINTENANCE':
                return 'status-maintenance';
            default:
                return 'status-available';
        }
    }

    function formatRoomType(type) {
        if (!type) return 'Standard';
        return type.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
    }

    function getInitials(name) {
        if (!name) return 'S';
        const parts = name.trim().split(' ');
        if (parts.length >= 2) {
            return (parts[0][0] + parts[1][0]).toUpperCase();
        }
        return name.slice(0, 2).toUpperCase();
    }

    function escapeHtml(str) {
        if (str === null || str === undefined) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Initial Load
    fetchAllData();
    // Auto-refresh health every 30 seconds
    setInterval(checkHealth, 30000);
});
