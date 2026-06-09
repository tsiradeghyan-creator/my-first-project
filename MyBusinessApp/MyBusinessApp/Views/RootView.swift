import SwiftUI

struct RootView: View {
    var body: some View {
        TabView {
            DashboardView()
                .tabItem { Label("Earnings", systemImage: "chart.line.uptrend.xyaxis") }

            OfferingsView()
                .tabItem { Label("Offerings", systemImage: "bag") }

            ProfileView()
                .tabItem { Label("Profile", systemImage: "person.crop.circle") }
        }
    }
}

#Preview {
    RootView().environmentObject(AppStore())
}
