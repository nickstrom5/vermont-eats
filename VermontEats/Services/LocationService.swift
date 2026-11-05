import CoreLocation
import Observation
import UIKit

/// "Near me" sorting. Asks for when-in-use permission only when a list is sorted by distance or "My location" is tapped; the location never leaves the device.
@MainActor
@Observable
final class LocationService: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    private(set) var location: CLLocation?
    private(set) var status: CLAuthorizationStatus = .notDetermined
    /// no fix within 12 seconds, or Core Location reported an error
    private(set) var failed = false
    private var timeout: Task<Void, Never>?
    /// when the current request started: a fix from before it is a cached one (from launch, or before a drive) and doesn't count
    private var askedAt = Date.distantPast

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        status = manager.authorizationStatus
    }

    var isDenied: Bool { status == .denied || status == .restricted }

    /// Every place is in Vermont, so a reader elsewhere (an App Reviewer in California, say) gets told rather than an empty map.
    /// A coarse outline of the state (Idaho's lesson: a bounding box would count Hanover, Plattsburgh and Stanstead), drawn a little
    /// outside the line so the river and lake shores count as inside.
    var isOutsideVermont: Bool {
        guard let c = location?.coordinate else { return false }
        return !VermontOutline.contains(c)
    }

    /// Once location is off for the app, iOS won't ask again; the app's page in Settings is the only way back.
    static func openSettings() {
        if let url = URL(string: UIApplication.openSettingsURLString) { UIApplication.shared.open(url) }
    }

    func request() {
        switch manager.authorizationStatus {
        case .notDetermined: manager.requestWhenInUseAuthorization()
        case .authorizedWhenInUse, .authorizedAlways: locate()
        default: break
        }
    }

    private func locate() {
        failed = false
        let asked = Date()
        askedAt = asked
        manager.requestLocation()
        timeout?.cancel()
        timeout = Task { [weak self] in
            try? await Task.sleep(for: .seconds(12))
            guard let self, !Task.isCancelled else { return }
            if (self.location?.timestamp ?? .distantPast) < asked { self.failed = true }
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ m: CLLocationManager) {
        let s = m.authorizationStatus
        Task { @MainActor in
            self.status = s
            if s == .authorizedWhenInUse || s == .authorizedAlways { self.locate() }
        }
    }

    nonisolated func locationManager(_ m: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let l = locations.last else { return }
        Task { @MainActor in
            // "My location" needs a fresh fix on every tap: a cached one from before the request would put you back where you were
            guard l.timestamp >= self.askedAt.addingTimeInterval(-2) else { return }
            self.location = l; self.failed = false; self.timeout?.cancel()
        }
    }

    nonisolated func locationManager(_ m: CLLocationManager, didFailWithError error: Error) {
        Task { @MainActor in if self.location == nil { self.failed = true } }
    }
}

extension CLLocation {
    /// "0.4 mi", "12 mi", "1,012 mi" (an App Reviewer in California is a thousand miles out)
    func milesText(to other: CLLocation) -> String {
        let mi = distance(from: other) / 1609.344
        return (mi < 10 ? mi.formatted(.number.precision(.fractionLength(1))) : Int(mi.rounded()).formatted()) + " mi"
    }
}

/// A coarse Vermont outline (longitude, latitude), about 600 m outside the Overture land outline (buffer 0.006°, simplify 0.01°; it
/// follows the state line through Lake Champlain, so the islands are inside). Burlington, Isle La Motte, Derby Line, Norwich, White
/// River Junction, Bellows Falls, Brattleboro and Bennington are inside; Hanover and Lebanon (New Hampshire), Plattsburgh (New York),
/// Stanstead (Quebec), Walpole and Hinsdale (New Hampshire) and Williamstown (Massachusetts) are not.
enum VermontOutline {
    static let rings: [[(Double, Double)]] = [
        [(-73.437, 43.585), (-73.432, 43.645), (-73.358, 43.771), (-73.398, 43.819), (-73.381, 43.876), (-73.414, 43.929),
         (-73.413, 44.019), (-73.444, 44.046), (-73.396, 44.194), (-73.319, 44.266), (-73.341, 44.365), (-73.3, 44.439),
         (-73.312, 44.498), (-73.379, 44.572), (-73.396, 44.618), (-73.37, 44.692), (-73.371, 44.744), (-73.339, 44.788),
         (-73.388, 44.849), (-73.345, 44.92), (-73.344, 44.962), (-73.361, 44.986), (-73.347, 45.016), (-71.46, 45.017),
         (-71.479, 44.997), (-71.528, 44.994), (-71.489, 44.902), (-71.542, 44.861), (-71.546, 44.834), (-71.57, 44.816),
         (-71.569, 44.787), (-71.622, 44.749), (-71.58, 44.662), (-71.542, 44.633), (-71.548, 44.606), (-71.529, 44.59),
         (-71.557, 44.559), (-71.591, 44.557), (-71.566, 44.54), (-71.581, 44.518), (-71.572, 44.499), (-71.635, 44.469),
         (-71.701, 44.408), (-71.792, 44.393), (-71.813, 44.349), (-71.871, 44.331), (-71.905, 44.342), (-71.98, 44.331),
         (-72.026, 44.316), (-72.055, 44.282), (-72.042, 44.238), (-72.059, 44.191), (-72.027, 44.132), (-72.049, 44.11),
         (-72.026, 44.103), (-72.026, 44.076), (-72.108, 43.992), (-72.086, 43.963), (-72.18, 43.86), (-72.178, 43.808),
         (-72.2, 43.768), (-72.294, 43.703), (-72.297, 43.667), (-72.329, 43.618), (-72.323, 43.598), (-72.375, 43.571),
         (-72.393, 43.513), (-72.376, 43.478), (-72.41, 43.376), (-72.384, 43.358), (-72.404, 43.331), (-72.39, 43.312),
         (-72.433, 43.251), (-72.45, 43.147), (-72.427, 43.121), (-72.428, 43.085), (-72.461, 43.051), (-72.438, 43.006),
         (-72.47, 42.967), (-72.527, 42.951), (-72.519, 42.914), (-72.549, 42.874), (-72.536, 42.811), (-72.472, 42.765),
         (-72.455, 42.722), (-73.28, 42.741), (-73.297, 42.802), (-73.284, 42.841), (-73.249, 43.533), (-73.264, 43.56),
         (-73.302, 43.576), (-73.309, 43.618), (-73.364, 43.618), (-73.379, 43.573), (-73.398, 43.562)]]

    static func contains(_ c: CLLocationCoordinate2D) -> Bool { rings.contains { contains(c, ring: $0) } }

    /// Ray casting: a point is inside when a ray east of it crosses the outline an odd number of times.
    static func contains(_ c: CLLocationCoordinate2D, ring: [(Double, Double)]) -> Bool {
        var inside = false
        var j = ring.count - 1
        for i in 0..<ring.count {
            let (xi, yi) = ring[i], (xj, yj) = ring[j]
            if (yi > c.latitude) != (yj > c.latitude) && c.longitude < (xj - xi) * (c.latitude - yi) / (yj - yi) + xi { inside.toggle() }
            j = i
        }
        return inside
    }
}
