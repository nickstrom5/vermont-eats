import Foundation
import CoreLocation
import UIKit

/// `-screenshot <name>` opens one screen with fixed state for App Store screenshots (scripts/capture-screenshots.sh).
/// Names: home, diners, creemees, cider, pizza, sugarhouses, taprooms, inns, honors, oldest, detail, map, saved, about.
enum ScreenshotMode {
    /// Debug builds only: an App Store build ignores the launch argument, so no one can reach seeded screens or fake locations.
    static var name: String? {
        #if DEBUG
        let args = ProcessInfo.processInfo.arguments
        guard let i = args.firstIndex(of: "-screenshot"), i + 1 < args.count else { return nil }
        return args[i + 1]
        #else
        return nil
        #endif
    }
    static var isActive: Bool { name != nil }

    @MainActor
    static func apply(to model: AppModel) {
        guard let name, model.isLoaded else { return }
        model.filters = Filters()
        // downtown Burlington (Church Street), so "nearest" lists have distances without a permission prompt
        model.screenshotLocation = CLLocation(latitude: 44.4780, longitude: -73.2130)
        // by name and town, ignoring case, so a rebuild with a slightly different casing still finds the place; the hand-checked one first
        let pick = { (n: String, town: String?) -> Place? in
            let hits = model.places.filter { $0.name.caseInsensitiveCompare(n) == .orderedSame && (town == nil || $0.city == town) }
            return hits.first(where: \.handChecked) ?? hits.first
        }
        for p in [pick("Al's French Frys", "South Burlington"), pick("Morse Farm Maple Sugarworks", "Montpelier"), pick("Henry's Diner", "Burlington")]
            .compactMap({ $0 }) where !model.isSaved(p) {
            model.toggleSaved(p)
        }
        let open = { (g: Guide) in model.tab = .guides; model.selectedGuide = g; model.guidesPath = [.guide(g)] }
        switch name {
        case "diners": open(.diners)
        case "creemees":
            // Montpelier, central to the creemee stands (Morse Farm, Waitsfield, Williamstown, Randolph)
            model.screenshotLocation = CLLocation(latitude: 44.2601, longitude: -72.5754)
            open(.creemees)
        case "cider": open(.cider)
        case "pizza": open(.pizza)
        case "sugarhouses": open(.sugarhouses)
        case "taprooms":
            // Waitsfield, in the Mad River Valley
            model.screenshotLocation = CLLocation(latitude: 44.1900, longitude: -72.8240)
            open(.taprooms)
        case "inns":
            // Woodstock, among the Windsor County inns
            model.screenshotLocation = CLLocation(latitude: 43.6242, longitude: -72.5185)
            open(.inns)
        case "honors": open(.honors)
        case "oldest": open(.oldest)
        case "detail":
            // Al's French Frys: a fry stand, a James Beard America's Classic and a 1946 founding year, with its note
            open(.diners)
            if let p = pick("Al's French Frys", "South Burlington") ?? model.places.first {
                model.selectedPlace = p; model.guidesPath.append(.place(p))
            }
        case "map": model.tab = .map
        case "saved": model.tab = .saved
        case "about": model.tab = .about
        default: model.tab = .guides; model.selectedGuide = nil
        }
        // iPad shows the place column next to every list, so give each shot a place instead of "Pick a place": a different
        // honored or hand-checked one per shot.
        guard UIDevice.current.userInterfaceIdiom == .pad, model.selectedPlace == nil else { return }
        let place: Place? = switch name {
        case "home": pick("Al's French Frys", "South Burlington")
        case "diners": pick("Henry's Diner", "Burlington")
        case "creemees": pick("Canteen Creemee Company", "Waitsfield")
        case "cider": pick("Cold Hollow Cider Mill", "Waterbury")
        case "pizza": pick("Woodbelly Pizza", "Middlesex")
        case "sugarhouses": pick("Morse Farm Maple Sugarworks", "Montpelier")
        case "taprooms": pick("Lawson's Finest Liquids", "Waitsfield")
        case "inns": pick("Ye Olde Tavern", "Manchester")
        case "map": pick("Henry's Diner", "Burlington")
        case "honors": pick("Saap", "Randolph")
        case "oldest": pick("Ye Olde Tavern", "Manchester")
        case "saved": pick("Morse Farm Maple Sugarworks", "Montpelier")
        case "about": nil
        default: pick("Al's French Frys", "South Burlington")
        }
        model.selectedPlace = place
    }
}
