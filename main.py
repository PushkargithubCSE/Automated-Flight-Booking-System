import sys
import os
import json
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

# --- MOCK FUNCTION if you don't have a custom passenger generator ---
def generate_passenger():
    """Generates a dummy passenger dictionary."""
    return {
        "name": "John Doe",
        "email": "john.doe.example@email.com",
        "phone": "9876543210"
    }
# --------------------------------------------------------------------

# Add local packages folder if using
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "packages"))


def open_website(page):
    """Opens the MakeMyTrip flights page and handles initial popups."""
    print("Navigating to MakeMyTrip...")
    page.goto("https://www.makemytrip.com/flights/", timeout=60000)
    page.wait_for_load_state("load")

    frame_locator = page.frame_locator("[title*='notification-frame']")
    if frame_locator.locator("a.close").is_visible(timeout=5000):
        frame_locator.locator("a.close").click()

    page.locator("body").click(position={'x': 0, 'y': 0}, delay=200)
    print("Opened MakeMyTrip Flight Page ✅")


def search_flights(page, source, destination, travel_date_str):
    """Searches for flights using robust selectors and correct date formatting."""
    print(f"Searching flights from {source} → {destination} on {travel_date_str}")

    # --- FROM ---
    page.locator("#fromCity").click()
    page.get_by_placeholder("From").fill(source)
    page.locator(f"li[id*='react-autowhatever']").filter(has_text=source).first.click()
    print(f"Selected source: {source}")

    # --- TO ---
    page.locator("#toCity").click()
    page.get_by_placeholder("To").fill(destination)
    page.locator(f"li[id*='react-autowhatever']").filter(has_text=destination).first.click()
    print(f"Selected destination: {destination}")

    # --- DATE ---
    date_obj = datetime.strptime(travel_date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%a %b %d %Y")

    date_selector = f"div[aria-label='{formatted_date}']"
    date_element = page.locator(date_selector).first
    expect(date_element).to_be_visible(timeout=30000)
    date_element.click()
    print(f"Selected date: {formatted_date}")

    # --- SEARCH ---
    search_btn = page.locator("a", has_text="Search").first
    expect(search_btn).to_be_visible(timeout=30000)
    search_btn.click()

    if page.locator(".fareLockInfoContainer").is_visible(timeout=15000):
        page.locator(".fareLockCta .button button").click()
        print("Closed 'OKAY, GOT IT!' popup.")


def scrape_flights(page):
    """Scrapes all flight data from the search results page."""
    print("Scraping flight results...")
    
    listing_container_selector = 'div[id*="listing-id"]'
    page.wait_for_selector(listing_container_selector, timeout=60000)

    flight_elements = page.locator(".makeFlex.h-full.relative.one-way-listing").all()
    flight_data = []

    if not flight_elements:
        print("No flight elements found on the page.")
        return None

    for flight in flight_elements:
        try:
            airline = flight.locator(".airline-info .airlineName").inner_text()
            dep_time = flight.locator(".time-group .depart-time").inner_text()
            arr_time = flight.locator(".time-group .arrival-time").inner_text()
            duration = flight.locator(".stop-info .total-duration").inner_text()
            price = flight.locator(".price-section .cluster-price-revamp").inner_text()

            cleaned_price = int("".join(filter(str.isdigit, price)))

            flight_data.append({
                "airline": airline,
                "departure": dep_time,
                "arrival": arr_time,
                "duration": duration,
                "price": cleaned_price
            })
        except Exception:
            continue

    if not flight_data:
        print("No flights found or couldn't scrape any flights.")
        return None

    if not os.path.exists("output"):
        os.makedirs("output")
    with open("output/all_flights.json", "w") as f:
        json.dump(flight_data, f, indent=4)

    print(f"Scraped {len(flight_data)} flights ✅")
    return flight_data


def save_booking(flight, passenger):
    """Saves the final selected flight and passenger details to a JSON file."""
    if not os.path.exists("output"):
        os.makedirs("output")

    booking = {
        "flight_details": flight,
        "passenger_details": passenger
    }
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/booking_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(booking, f, indent=4)
    print(f"Saved booking details to {filename} ✅")


def main():
    """Main function to run the flight booking automation."""
    source = "Delhi"
    destination = "Mumbai"
    # Ensure this date is in the future to avoid errors on the website
    travel_date = "2025-10-05"

    with sync_playwright() as p:
        # Increased slow_mo to make it easier to watch
        browser = p.chromium.launch(headless=False, slow_mo=250)
        page = browser.new_page()

        try:
            open_website(page)
            search_flights(page, source, destination, travel_date)

            # --- PAUSING FOR DEBUGGING ---
            print("\n>>> SCRIPT PAUSED <<<")
            print("The Playwright Inspector is now open.")
            print("Look at the browser window to see what's on the page.")
            print("Close the Inspector window to continue the script.")
            
            # This line will pause the script and open the inspector
            page.pause()

            # The script will resume here after you close the inspector
            print("\nResuming script...")
            
            # Now, we explicitly wait for the URL to change to the results page
            print("Waiting for search results page URL...")
            page.wait_for_url("**/flight/search/**", timeout=60000)
            print("Search results page loaded successfully!")

            # We will try scraping again after confirming the page loads
            flights = scrape_flights(page)

            if flights:
                cheapest_flight = min(flights, key=lambda x: x['price'])
                passenger = generate_passenger()
                print(f"\nCheapest flight found: {cheapest_flight['airline']} at ₹{cheapest_flight['price']}")
                save_booking(cheapest_flight, passenger)
                print("\nAutomation finished successfully!")
            else:
                print("\nCould not proceed as no flights were scraped.")

        except Exception as e:
            # On any error, print the error
            print(f"\nAn error occurred: {e}")
            # Screenshot is disabled temporarily as it was causing its own timeout

        finally:
            print("\nClosing browser in 10 seconds...")
            page.wait_for_timeout(10000)
            browser.close()


if __name__ == "__main__":
    main()