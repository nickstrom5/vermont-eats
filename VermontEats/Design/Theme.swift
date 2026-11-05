import SwiftUI
import UIKit
import CoreText

/// Vermont palette, a landscape one (provisional, 2026-11-05; Nick decides, playbook/05-naming.md), light only. No major-league team
/// plays here and fans split among Boston, New York and Montreal, so the colors come from the land (state-prompts/VERMONT_PROMPT.md):
/// spruce #1E4D2B (9.8:1 on white) for titles, tint and accents; maple amber #A0521D (white on it 5.7:1) for the hand-checked guide
/// cards under white text; barn red #9E2A2B (7.5:1) for honors chips; syrup gold #D9A441 only as a pin and card fill under ink
/// #1A1A1A (7.7:1); a cream #FAF7F0 page. The names `green`/`gold` are kept from Wisconsin Eats so the shared views read the same;
/// here `green` is spruce and `gold` is maple amber.
enum Theme {
    static let green = Color(hex: 0x1E4D2B)      // spruce: titles, tint, primary text accents
    static let green2 = Color(hex: 0x2F6B3E)
    static let gold = Color(hex: 0xA0521D)       // maple amber: card fills under white text, chips
    static let goldSoft = Color(hex: 0xF3E3D3)   // soft amber
    static let lime = Color(hex: 0xD9A441)       // syrup gold, fills only (hand-checked pins, the title shadow), under ink
    static let limeSoft = Color(hex: 0xF7EBCD)
    static let sand = Color(hex: 0xFAF7F0)       // the Home background, cream
    static let red = Color(hex: 0x9E2A2B)        // barn red: honors chips
    static let sandstone = Color(hex: 0x9E2A2B)  // barn-red accent (7.5:1 on white)
    static let teal = Color(hex: 0x2C5F7C)       // Lake Champlain accent (6.6:1 on white)
    static let ink = Color(hex: 0x1A1A1A)
    static let ink2 = Color(hex: 0x2E3440)
    static let muted = Color(hex: 0x5B6270)
    static let surface = Color.white
    static let surface2 = Color(hex: 0xF1EEE6)
    static let surface3 = Color(hex: 0xE4DFD3)
    static let rule = Color(hex: 0xE4DFD3)
    static let rule2 = Color(hex: 0xCCC4B3)
}

extension Color {
    init(hex: UInt32) {
        self.init(red: Double((hex >> 16) & 0xFF) / 255, green: Double((hex >> 8) & 0xFF) / 255, blue: Double(hex & 0xFF) / 255)
    }
}

/// A small uppercase label: "STONE CRAB", "1 MICHELIN STAR".
struct Chip: View {
    enum Style { case gold, green, red, plain, dashed }
    let text: String
    var style: Style = .plain

    var body: some View {
        Text(text.uppercased())
            .font(.caption2.weight(.bold))
            .tracking(0.4)
            .padding(.horizontal, 7).padding(.vertical, 3)
            .foregroundStyle(style == .green || style == .red ? Color.white : style == .dashed ? Theme.muted : style == .gold ? Theme.ink : Theme.green)
            .background {
                RoundedRectangle(cornerRadius: 5).fill(style == .gold ? Theme.goldSoft : style == .green ? Theme.green : style == .red ? Theme.red
                                                       : style == .dashed ? .clear : Theme.surface2)
            }
            .overlay {
                if style == .dashed { RoundedRectangle(cornerRadius: 5).strokeBorder(Theme.rule2, style: StrokeStyle(lineWidth: 1, dash: [3, 2])) }
            }
            .accessibilityLabel(text)
    }
}

/// Green Mountain Eats' lettering: the system face drawn compressed and heavy for titles and guide names (like a show poster), and the
/// system monospaced face for numbers, dates and small labels. No bundled fonts.
struct DisplayFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .black
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight).width(.compressed))
    }
}

/// Numbers, dates and small labels in the system monospaced face, scaled like DisplayFont.
struct MonoFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .semibold
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight, design: .monospaced))
    }
}

extension View {
    func displayFont(_ size: CGFloat, weight: Font.Weight = .black) -> some View {
        modifier(DisplayFont(size: size, weight: weight))
    }

    func monoFont(_ size: CGFloat, weight: Font.Weight = .semibold) -> some View {
        modifier(MonoFont(size: size, weight: weight))
    }
}

/// The header band: the Green Mountains' ridgeline in spruce, rising to Camel's Hump (its long north slope and the sharp drop to the
/// south) at the right of center, over a maple-amber baseline.
struct Stripes: View {
    var height: CGFloat = 6

    /// (x, rise) across the band: 0 is the baseline, 1 the summit
    static let ridge: [(CGFloat, CGFloat)] = [(0, 0.35), (0.08, 0.5), (0.16, 0.38), (0.26, 0.55), (0.36, 0.45), (0.46, 0.62), (0.55, 0.78),
                                              (0.61, 1.0), (0.635, 0.97), (0.67, 0.55), (0.74, 0.48), (0.82, 0.6), (0.9, 0.42), (1, 0.5)]

    var body: some View {
        Canvas { ctx, size in
            let w = size.width, h = size.height, base = h * 0.78
            var hills = Path()
            hills.move(to: CGPoint(x: 0, y: base))
            for (x, rise) in Self.ridge { hills.addLine(to: CGPoint(x: x * w, y: base - base * rise)) }
            hills.addLine(to: CGPoint(x: w, y: base))
            hills.closeSubpath()
            ctx.fill(hills, with: .color(Theme.green))
            // the maple-amber baseline last
            ctx.fill(Path(CGRect(x: 0, y: base, width: w, height: h - base)), with: .color(Theme.gold))
        }
        .frame(height: height * 2.4)
        .clipShape(RoundedRectangle(cornerRadius: 3))
        .accessibilityHidden(true)
    }
}

extension View {
    /// An inline navigation title in the display type. UINavigationBar.appearance() didn't reach every SwiftUI bar on iOS 27
    /// (the Map title went from compressed blue to plain black after a push and pop; place titles were always plain), so the
    /// title is our own view in the bar. The navigation title is still set, for the back button and VoiceOver.
    func inlineTitle(_ title: String) -> some View {
        navigationTitle(title)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    Text(title).displayFont(19, weight: .heavy).foregroundStyle(Theme.green)
                        .lineLimit(1).minimumScaleFactor(0.7)
                        .accessibilityAddTraits(.isHeader)
                }
            }
    }
}
