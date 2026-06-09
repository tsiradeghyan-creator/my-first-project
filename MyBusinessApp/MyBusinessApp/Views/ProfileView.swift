import SwiftUI

struct ProfileView: View {
    @EnvironmentObject var store: AppStore

    var body: some View {
        NavigationStack {
            List {
                Section("Your business") {
                    LabeledContent("Offerings", value: "\(store.offerings.count)")
                    LabeledContent("Sales", value: "\(store.sales.count)")
                    LabeledContent("Total earned",
                                   value: store.totalEarnings.formatted(.currency(code: "USD")))
                }

                Section("Next steps") {
                    Text("1. Replace the sample offerings with your real products or services.")
                    Text("2. Connect a payment provider (Apple In-App Purchase or Stripe).")
                    Text("3. Add a way for customers to discover you (marketing).")
                }
            }
            .navigationTitle("Profile")
        }
    }
}

#Preview {
    ProfileView().environmentObject(AppStore())
}
