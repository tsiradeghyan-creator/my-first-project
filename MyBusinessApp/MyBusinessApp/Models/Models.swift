import Foundation

/// A product or service your app sells. Money is earned when a customer
/// buys one of these — this is the real source of income, not the app itself.
struct Offering: Identifiable, Codable {
    let id: UUID
    var title: String
    var details: String
    var price: Decimal

    init(id: UUID = UUID(), title: String, details: String, price: Decimal) {
        self.id = id
        self.title = title
        self.details = details
        self.price = price
    }
}

/// A completed sale. The earnings dashboard sums these up.
struct Sale: Identifiable, Codable {
    let id: UUID
    var offeringTitle: String
    var amount: Decimal
    var date: Date

    init(id: UUID = UUID(), offeringTitle: String, amount: Decimal, date: Date = .now) {
        self.id = id
        self.offeringTitle = offeringTitle
        self.amount = amount
        self.date = date
    }
}
