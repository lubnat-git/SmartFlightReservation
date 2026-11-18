
const API_URL = "http://127.0.0.1:8000";


// ==========================================
// HELPER: GET LOGIN TOKEN
// ==========================================

function getToken() {
    return localStorage.getItem("access_token");
}


// ==========================================
// 1. USER REGISTRATION
// ==========================================

window.registerUser = async function () {

    const fullName = document.getElementById("registerName").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value;

    const message = document.getElementById("registerMessage");

    if (!fullName || !email || !password) {
        message.textContent = "Please fill in all fields.";
        return;
    }

    try {

        const response = await fetch(API_URL + "/auth/register", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                full_name: fullName,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {

            message.textContent = "Registration successful!";

        } else {

            message.textContent =
                data.detail || "Registration failed.";

        }

    } catch (error) {

        message.textContent = "Unable to connect to server.";

        console.error(error);

    }
};


// ==========================================
// 2. USER LOGIN
// ==========================================

window.loginUser = async function () {

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    const message = document.getElementById("loginMessage");

    if (!email || !password) {

        message.textContent = "Please enter email and password.";

        return;
    }

    try {

        const response = await fetch(API_URL + "/auth/login", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {

            localStorage.setItem("access_token", data.access_token);

            message.textContent = "Login successful!";

        } else {

            message.textContent =
                data.detail || "Login failed.";

        }

    } catch (error) {

        message.textContent = "Unable to connect to server.";

        console.error(error);

    }
};


// ==========================================
// 3. SEARCH FLIGHTS
// ==========================================

window.searchFlights = async function () {

    const sourceCity =
        document.getElementById("sourceCity").value.trim();

    const destinationCity =
        document.getElementById("destinationCity").value.trim();

    const resultsDiv =
        document.getElementById("flightResults");

    if (!sourceCity || !destinationCity) {

        resultsDiv.textContent =
            "Please enter both source and destination cities.";

        return;
    }

    resultsDiv.textContent = "Searching for flights...";

    try {

        const response = await fetch(
            API_URL + "/search?source_city=" +
            encodeURIComponent(sourceCity) +
            "&destination_city=" +
            encodeURIComponent(destinationCity)
        );

        const data = await response.json();

        resultsDiv.innerHTML = "";

        if (
            response.ok &&
            data.flights &&
            data.flights.length > 0
        ) {

            data.flights.forEach(function (flight) {

                const flightCard = document.createElement("div");

                flightCard.style.border = "1px solid #ccc";
                flightCard.style.padding = "15px";
                flightCard.style.margin = "10px 0";
                flightCard.style.borderRadius = "8px";

                const details = document.createElement("p");

                details.textContent =
                    "Flight: " + flight.flight_number +
                    " | Airline: " + flight.airline_name +
                    " | From: " + flight.source_city +
                    " | To: " + flight.destination_city +
                    " | Price: ₹" + flight.price +
                    " | Available Seats: " + flight.seats_available;

                flightCard.appendChild(details);

                const bookButton = document.createElement("button");

                bookButton.type = "button";

                bookButton.textContent = "Book Flight";

                bookButton.onclick = function () {

                    window.bookFlight(flight.flight_id);

                };

                flightCard.appendChild(bookButton);

                resultsDiv.appendChild(flightCard);

            });

        } else {

            resultsDiv.textContent = "No flights found.";

        }

    } catch (error) {

        resultsDiv.textContent = "Unable to connect to server.";

        console.error(error);

    }
};


// ==========================================
// 4. BOOK A FLIGHT
// ==========================================

window.bookFlight = async function (flightId) {

    const token = getToken();

    const passengerId =
        document.getElementById("passengerId").value;

    if (!token) {

        alert("Please login before booking.");

        return;
    }

    if (!passengerId || Number(passengerId) <= 0) {

        alert("Please enter a valid Passenger ID.");

        return;
    }

    const confirmation = confirm(
        "Do you want to book this flight?"
    );

    if (!confirmation) {
        return;
    }

    try {

        const response = await fetch(API_URL + "/bookings/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },

            body: JSON.stringify({
                flight_id: flightId,
                passenger_id: Number(passengerId)
            })

        });

        const data = await response.json();

        if (response.ok) {

            alert(
                "Booking successful!\n" +
                "Booking ID: " + data.booking_id +
                "\nSeat Number: " + data.seat_number
            );

            window.loadBookings();

        } else {

            alert(data.detail || "Booking failed.");

        }

    } catch (error) {

        alert("Unable to connect to server.");

        console.error(error);

    }
};


// ==========================================
// 5. VIEW MY BOOKINGS
// ==========================================

window.loadBookings = async function () {

    const token = getToken();

    const resultsDiv =
        document.getElementById("bookingResults");

    if (!token) {

        resultsDiv.textContent = "Please login first.";

        return;
    }

    resultsDiv.textContent = "Loading bookings...";

    try {

        const response = await fetch(API_URL + "/bookings/my", {

            method: "GET",

            headers: {
                "Authorization": "Bearer " + token
            }

        });

        const data = await response.json();

        resultsDiv.innerHTML = "";

        if (!response.ok) {

            resultsDiv.textContent =
                data.detail || "Unable to load bookings.";

            return;
        }

        if (!data.bookings || data.bookings.length === 0) {

            resultsDiv.textContent = "No bookings found.";

            return;
        }

        data.bookings.forEach(function (booking) {

            const card = document.createElement("div");

            card.style.border = "1px solid #ccc";
            card.style.padding = "15px";
            card.style.margin = "10px 0";
            card.style.borderRadius = "8px";

            const details = document.createElement("p");

            details.textContent =
                "Booking ID: " + booking.booking_id +
                " | Flight: " + (booking.flight_number || "") +
                " | From: " + (booking.source_city || "") +
                " | To: " + (booking.destination_city || "") +
                " | Seat: " + (booking.seat_number || "") +
                " | Status: " + booking.status;

            card.appendChild(details);

            if (
                String(booking.status).toLowerCase() !== "cancelled"
            ) {

                const cancelButton = document.createElement("button");

                cancelButton.type = "button";

                cancelButton.textContent = "Cancel Booking";

                cancelButton.onclick = function () {

                    window.cancelBooking(booking.booking_id);

                };

                card.appendChild(cancelButton);

            }

            resultsDiv.appendChild(card);

        });

    } catch (error) {

        resultsDiv.textContent = "Unable to connect to server.";

        console.error(error);

    }
};


// ==========================================
// 6. CANCEL BOOKING
// ==========================================

window.cancelBooking = async function (bookingId) {

    const token = getToken();

    if (!token) {

        alert("Please login first.");

        return;
    }

    if (!confirm("Are you sure you want to cancel this booking?")) {

        return;
    }

    try {

        const response = await fetch(
            API_URL + "/bookings/cancel/" + bookingId,
            {

                method: "PUT",

                headers: {
                    "Authorization": "Bearer " + token
                }

            }
        );

        const data = await response.json();

        if (response.ok) {

            alert("Booking cancelled successfully!");

            window.loadBookings();

        } else {

            alert(data.detail || "Cancellation failed.");

        }

    } catch (error) {

        alert("Unable to connect to server.");

        console.error(error);

    }
};


// ==========================================
// 7. SIMULATED PAYMENT
// ==========================================

window.makePayment = async function () {

    const token = getToken();

    const bookingId =
        document.getElementById("bookingId").value;

    const mode =
        document.getElementById("paymentMode").value;

    const message =
        document.getElementById("paymentMessage");

    if (!token) {

        message.textContent = "Please login before making payment.";

        return;
    }

    if (!bookingId || Number(bookingId) <= 0) {

        message.textContent = "Please enter a valid Booking ID.";

        return;
    }

    message.textContent = "Processing simulated payment...";

    try {

        const response = await fetch(API_URL + "/payments/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },

            body: JSON.stringify({
                booking_id: Number(bookingId),
                mode: mode
            })

        });

        const data = await response.json();

        if (response.ok) {

            message.textContent = "Payment successful!";

        } else {

            message.textContent =
                data.detail || "Payment failed.";

        }

    } catch (error) {

        message.textContent = "Unable to connect to server.";

        console.error(error);

    }
};


// ==========================================
// 8. AI TRAVEL ASSISTANT
// ==========================================

// Create and display a chat message safely.

function addChatMessage(message, className) {

    const chatMessages =
        document.getElementById("chatMessages");

    const messageElement = document.createElement("div");

    messageElement.className = "chat-message " + className;

    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageElement;
}


// Display knowledge-base source references.

function addChatSources(messageElement, sources) {

    if (!Array.isArray(sources) || sources.length === 0) {
        return;
    }

    const sourcesContainer = document.createElement("div");

    sourcesContainer.className = "chat-sources";

    const heading = document.createElement("strong");

    heading.textContent = "Sources:";

    sourcesContainer.appendChild(heading);

    const sourceList = document.createElement("ul");

    sourceList.className = "chat-source-list";

    sources.forEach(function (source) {

        const listItem = document.createElement("li");

        listItem.textContent = source;

        sourceList.appendChild(listItem);

    });

    sourcesContainer.appendChild(sourceList);

    messageElement.appendChild(sourcesContainer);
}


// Send a question to the FastAPI AI assistant.

window.sendChatMessage = async function () {

    const questionInput =
        document.getElementById("chatQuestion");

    const sendButton =
        document.getElementById("chatSendButton");

    const chatStatus =
        document.getElementById("chatStatus");

    const question = questionInput.value.trim();

    if (!question) {

        chatStatus.textContent =
            "Please enter a travel-related question.";

        return;
    }

    if (sendButton.disabled) {
        return;
    }

    chatStatus.textContent = "";

    // Display the user's question.

    addChatMessage(question, "user-message");

    // Show a loading message.

    const loadingMessage = addChatMessage(
        "Thinking... Please wait.",
        "assistant-message"
    );

    sendButton.disabled = true;

    sendButton.textContent = "Thinking...";

    try {

        const response = await fetch(API_URL + "/assistant/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        let data;

        try {

            data = await response.json();

        } catch (error) {

            throw new Error(
                "The server returned an invalid response."
            );

        }

        if (!response.ok) {

            const errorMessage =
                typeof data.detail === "string"
                    ? data.detail
                    : "The AI assistant request failed.";

            throw new Error(errorMessage);
        }

        // Display the AI-generated answer.

        loadingMessage.textContent =
            data.answer || "No answer was returned.";

        // Display source references.

        addChatSources(
            loadingMessage,
            data.sources
        );

        // Clear the question after a successful response.

        questionInput.value = "";

    } catch (error) {

        console.error("AI Assistant Error:", error);

        if (error instanceof TypeError) {

            loadingMessage.textContent =
                "Unable to connect to the AI assistant. " +
                "Please check that the backend server is running.";

        } else {

            loadingMessage.textContent =
                error.message || "Something went wrong. Please try again.";

        }

        chatStatus.textContent = "Please try again.";

    } finally {

        sendButton.disabled = false;

        sendButton.textContent = "Send Message";

        questionInput.focus();

        const chatMessages =
            document.getElementById("chatMessages");

        chatMessages.scrollTop = chatMessages.scrollHeight;

    }

};


// ==========================================
// 9. AI FLIGHT SEARCH AGENT
// ==========================================

// Display flight recommendations and booking buttons.

function displayAgentFlights(flights, resultsDiv) {

    if (!Array.isArray(flights) || flights.length === 0) {
        return;
    }

    const heading = document.createElement("h4");

    heading.textContent = "Flight Recommendations";

    resultsDiv.appendChild(heading);

    flights.forEach(function (flight) {

        const flightCard = document.createElement("div");

        flightCard.style.border = "1px solid #ccc";
        flightCard.style.padding = "15px";
        flightCard.style.margin = "10px 0";
        flightCard.style.borderRadius = "8px";

        const details = document.createElement("p");

        details.textContent =
            "Flight: " + flight.flight_number +
            " | Airline: " + flight.airline_name +
            " | From: " + flight.source_city +
            " | To: " + flight.destination_city +
            " | Departure: " + flight.departure_time +
            " | Arrival: " + flight.arrival_time +
            " | Price: ₹" + flight.price +
            " | Available Seats: " + flight.seats_available;

        flightCard.appendChild(details);

        const bookButton = document.createElement("button");

        bookButton.type = "button";

        bookButton.textContent = "Book This Flight";

        bookButton.onclick = function () {

            // Reuse the existing booking workflow.
            // It checks login, passenger ID and user confirmation.

            window.bookFlight(flight.flight_id);

        };

        flightCard.appendChild(bookButton);

        resultsDiv.appendChild(flightCard);

    });

}


// Send a natural-language request to the FastAPI flight agent.

window.sendAgentMessage = async function () {

    const questionInput =
        document.getElementById("agentQuestion");

    const sendButton =
        document.getElementById("agentSendButton");

    const resultsDiv =
        document.getElementById("agentResults");

    const question = questionInput.value.trim();

    if (!question) {

        resultsDiv.textContent =
            "Please enter a flight-related request.";

        return;
    }

    if (sendButton.disabled) {
        return;
    }

    resultsDiv.textContent = "AI agent is searching for flights...";

    sendButton.disabled = true;

    sendButton.textContent = "Searching...";

    try {

        const response = await fetch(API_URL + "/agent/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        let data;

        try {

            data = await response.json();

        } catch (error) {

            throw new Error(
                "The server returned an invalid response."
            );

        }

        if (!response.ok) {

            const errorMessage =
                typeof data.detail === "string"
                    ? data.detail
                    : "The AI flight agent request failed.";

            throw new Error(errorMessage);
        }

        resultsDiv.innerHTML = "";

        // Display the natural-language agent response.

        const answer = document.createElement("p");

        answer.textContent =
            data.answer || "No response was returned by the AI agent.";

        resultsDiv.appendChild(answer);

        // Display the tools selected by the AI agent.

        if (
            Array.isArray(data.tools_used) &&
            data.tools_used.length > 0
        ) {

            const toolsInfo = document.createElement("p");

            toolsInfo.textContent =
                "Tools used: " + data.tools_used.join(", ");

            resultsDiv.appendChild(toolsInfo);

        }

        // Display flight details and booking options.

        displayAgentFlights(data.flights, resultsDiv);

        questionInput.value = "";

    } catch (error) {

        console.error("AI Flight Agent Error:", error);

        if (error instanceof TypeError) {

            resultsDiv.textContent =
                "Unable to connect to the AI flight agent. " +
                "Please check that the backend server is running.";

        } else {

            resultsDiv.textContent =
                error.message || "Something went wrong. Please try again.";

        }

    } finally {

        sendButton.disabled = false;

        sendButton.textContent = "Find Flights";

    }

};


// ==========================================
// AI CHAT: ENTER KEY SUPPORT
// ==========================================

const chatQuestionInput =
    document.getElementById("chatQuestion");

if (chatQuestionInput) {

    chatQuestionInput.addEventListener("keydown", function (event) {

        if (event.key === "Enter" && !event.shiftKey) {

            event.preventDefault();

            window.sendChatMessage();

        }

    });

}


// ==========================================
// AI FLIGHT AGENT: ENTER KEY SUPPORT
// ==========================================

const agentQuestionInput =
    document.getElementById("agentQuestion");

if (agentQuestionInput) {

    agentQuestionInput.addEventListener("keydown", function (event) {

        if (event.key === "Enter" && !event.shiftKey) {

            event.preventDefault();

            window.sendAgentMessage();

        }

    });

}


// ==========================================
// APPLICATION STARTUP
// ==========================================

console.log("Smart Flight Reservation System loaded successfully!");
