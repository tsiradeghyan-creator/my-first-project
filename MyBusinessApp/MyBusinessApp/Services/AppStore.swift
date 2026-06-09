import Foundation

/// Holds the app's data and persists it on the device.
/// Replace the sample data with your own offerings, and connect a real
/// payment provider (Apple In-App Purchase, Stripe, etc.) where marked.
@MainActor
final class AppStore: ObservableObject {
    @Published var offerings: [Offering] = []
    @Published var sales: [Sale] = []

    private let offeringsKey = "offerings.v1"
    private let salesKey = "sales.v1"

    init() {
        load()
        if offerings.isEmpty {
            offerings = AppStore.sampleOfferings
        }
    }

    /// Total earned across all sales.
    var totalEarnings: Decimal {
        sales.reduce(0) { $0 + $1.amount }
    }

    /// Earnings for the current calendar day.
    var todaysEarnings: Decimal {
        let cal = Calendar.current
        return sales
            .filter { cal.isDateInToday($0.date) }
            .reduce(0) { $0 + $1.amount }
    }

    func recordSale(of offering: Offering) {
        // TODO: trigger a real payment here (StoreKit / Stripe) before recording.
        let sale = Sale(offeringTitle: offering.title, amount: offering.price)
        sales.insert(sale, at: 0)
        save()
    }

    func addOffering(_ offering: Offering) {
        offerings.append(offering)
        save()
    }

    func removeOfferings(at offsets: IndexSet) {
        offerings.remove(atOffsets: offsets)
        save()
    }

    // MARK: - Persistence

    private func save() {
        let encoder = JSONEncoder()
        if let data = try? encoder.encode(offerings) {
            UserDefaults.standard.set(data, forKey: offeringsKey)
        }
        if let data = try? encoder.encode(sales) {
            UserDefaults.standard.set(data, forKey: salesKey)
        }
    }

    private func load() {
        let decoder = JSONDecoder()
        if let data = UserDefaults.standard.data(forKey: offeringsKey),
           let decoded = try? decoder.decode([Offering].self, from: data) {
            offerings = decoded
        }
        if let data = UserDefaults.standard.data(forKey: salesKey),
           let decoded = try? decoder.decode([Sale].self, from: data) {
            sales = decoded
        }
    }

    static let sampleOfferings: [Offering] = [
        Offering(title: "Consulting hour", details: "One hour of expert advice.", price: 150),
        Offering(title: "Monthly subscription", details: "Premium access, billed monthly.", price: 30),
        Offering(title: "Done-for-you setup", details: "A complete setup service.", price: 500)
    ]
}
