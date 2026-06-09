import SwiftUI

struct OfferingsView: View {
    @EnvironmentObject var store: AppStore
    @State private var showingAdd = false

    var body: some View {
        NavigationStack {
            List {
                ForEach(store.offerings) { offering in
                    VStack(alignment: .leading, spacing: 6) {
                        HStack {
                            Text(offering.title).font(.headline)
                            Spacer()
                            Text(offering.price, format: .currency(code: "USD"))
                                .fontWeight(.semibold)
                        }
                        Text(offering.details)
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                        Button {
                            store.recordSale(of: offering)
                        } label: {
                            Label("Sell this", systemImage: "creditcard")
                        }
                        .buttonStyle(.borderedProminent)
                        .padding(.top, 4)
                    }
                    .padding(.vertical, 4)
                }
                .onDelete(perform: store.removeOfferings)
            }
            .navigationTitle("Offerings")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button { showingAdd = true } label: { Image(systemName: "plus") }
                }
            }
            .sheet(isPresented: $showingAdd) {
                AddOfferingView()
            }
        }
    }
}

struct AddOfferingView: View {
    @EnvironmentObject var store: AppStore
    @Environment(\.dismiss) var dismiss

    @State private var title = ""
    @State private var details = ""
    @State private var priceText = ""

    var body: some View {
        NavigationStack {
            Form {
                TextField("Title", text: $title)
                TextField("Details", text: $details)
                TextField("Price (USD)", text: $priceText)
                    .keyboardType(.decimalPad)
            }
            .navigationTitle("New offering")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        let price = Decimal(string: priceText) ?? 0
                        store.addOffering(Offering(title: title, details: details, price: price))
                        dismiss()
                    }
                    .disabled(title.isEmpty || priceText.isEmpty)
                }
            }
        }
    }
}

#Preview {
    OfferingsView().environmentObject(AppStore())
}
