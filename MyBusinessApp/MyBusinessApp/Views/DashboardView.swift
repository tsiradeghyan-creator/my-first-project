import SwiftUI

struct DashboardView: View {
    @EnvironmentObject var store: AppStore

    private var currency: String { "USD" }

    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Today")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                        Text(store.todaysEarnings, format: .currency(code: currency))
                            .font(.system(size: 40, weight: .bold, design: .rounded))
                        Text("Total: \(store.totalEarnings.formatted(.currency(code: currency)))")
                            .font(.footnote)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 8)
                }

                Section("Recent sales") {
                    if store.sales.isEmpty {
                        Text("No sales yet. Make a sale from the Offerings tab.")
                            .foregroundStyle(.secondary)
                    } else {
                        ForEach(store.sales) { sale in
                            HStack {
                                VStack(alignment: .leading) {
                                    Text(sale.offeringTitle)
                                    Text(sale.date, style: .date)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                                Spacer()
                                Text(sale.amount, format: .currency(code: currency))
                                    .fontWeight(.semibold)
                            }
                        }
                    }
                }
            }
            .navigationTitle("Earnings")
        }
    }
}

#Preview {
    DashboardView().environmentObject(AppStore())
}
