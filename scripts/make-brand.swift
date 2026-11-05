// Green Mountain Eats brand (provisional, 2026-11-05; Nick picks the name, icon and palette): the app icon is concept A of
// scripts/icon-concepts.swift, a maple creemee on a waffle cone, on spruce; the shared Eats Ranked icon style,
// state-prompts/ICON-STYLE.md, no backing shape. No state seal or arms, no maple leaf (it reads as Canada), no team or school marks.
// Usage, from vt-eats/: swift scripts/make-brand.swift   -> VermontEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png,
// docs/ favicons and touch icons, docs/og.png. scripts/make-site.py draws the same mark as its inline SVG: change both together.
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let SPRUCE: UInt32 = 0x1E4D2B, CREAM: UInt32 = 0xF3E3C3, AMBER: UInt32 = 0xC77A2A, TAN: UInt32 = 0xD9A441
let MAPLE: UInt32 = 0xA0521D, SNOW: UInt32 = 0xFAF7F0, SPRUCE2: UInt32 = 0x2F6B3E

/// A: the maple creemee. CoreGraphics y-up, s = canvas size. Identical to icon-concepts.swift's concept A.
func creemee(_ c: CGContext, _ s: CGFloat) {
    func P(_ x: CGFloat, _ y: CGFloat) -> CGPoint { CGPoint(x: x * s, y: y * s) }
    // the cone: a tan triangle, point down, with a cream rim band
    let cone = CGMutablePath()
    cone.move(to: P(0.30, 0.50)); cone.addLine(to: P(0.70, 0.50)); cone.addLine(to: P(0.50, 0.15)); cone.closeSubpath()
    c.setFillColor(rgb(TAN)); c.addPath(cone); c.fillPath()
    // the swirl: three tiers of maple soft-serve, widest at the bottom, and its curl on top
    c.setFillColor(rgb(AMBER))
    c.fillEllipse(in: CGRect(x: 0.27 * s, y: 0.445 * s, width: 0.46 * s, height: 0.14 * s))
    c.fillEllipse(in: CGRect(x: 0.32 * s, y: 0.54 * s, width: 0.36 * s, height: 0.13 * s))
    c.fillEllipse(in: CGRect(x: 0.375 * s, y: 0.625 * s, width: 0.25 * s, height: 0.115 * s))
    let curl = CGMutablePath()
    curl.move(to: P(0.445, 0.71)); curl.addLine(to: P(0.555, 0.71)); curl.addLine(to: P(0.515, 0.84)); curl.closeSubpath()
    c.addPath(curl); c.fillPath()
    // the cream highlight bands between the tiers
    c.setFillColor(rgb(CREAM))
    c.fill(CGRect(x: 0.35 * s, y: 0.535 * s, width: 0.30 * s, height: 0.018 * s))
    c.fill(CGRect(x: 0.41 * s, y: 0.615 * s, width: 0.18 * s, height: 0.016 * s))
}


func render(_ n: Int, _ path: String, background: Bool) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: background ? CGImageAlphaInfo.noneSkipLast.rawValue : CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.setShouldAntialias(true)
    if background { ctx.setFillColor(rgb(SPRUCE)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n)) }
    creemee(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
render(1024, "VermontEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png", background: true)
try? FileManager.default.createDirectory(atPath: "docs", withIntermediateDirectories: true)
for (n, name) in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")] {
    render(n, "docs/" + name, background: true)
}

/// The share image (1200 x 630): spruce, the creemee at the left, the name and tagline at the right, and the app's header band
/// along the bottom: the Green Mountains' ridgeline rising to Camel's Hump, over a maple-amber baseline, on cream.
func og(_ path: String) {
    let W = 1200, H = 630
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(SPRUCE)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    // the band (y-up): cream ground, the ridgeline, the maple-amber baseline (Theme.swift's Stripes.ridge)
    let band: CGFloat = 70, base: CGFloat = 14
    ctx.setFillColor(rgb(SNOW)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: Int(band)))
    let ridge: [(CGFloat, CGFloat)] = [(0, 0.35), (0.08, 0.5), (0.16, 0.38), (0.26, 0.55), (0.36, 0.45), (0.46, 0.62), (0.55, 0.78),
                                       (0.61, 1.0), (0.635, 0.97), (0.67, 0.55), (0.74, 0.48), (0.82, 0.6), (0.9, 0.42), (1, 0.5)]
    let hills = CGMutablePath(); hills.move(to: CGPoint(x: 0, y: base))
    for (x, rise) in ridge { hills.addLine(to: CGPoint(x: x * CGFloat(W), y: base + (band - base) * rise)) }
    hills.addLine(to: CGPoint(x: CGFloat(W), y: base)); hills.closeSubpath()
    ctx.setFillColor(rgb(SPRUCE2)); ctx.addPath(hills); ctx.fillPath()
    ctx.setFillColor(rgb(MAPLE)); ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(W), height: base))
    ctx.saveGState(); ctx.translateBy(x: 40, y: 90); creemee(ctx, 500); ctx.restoreGState()
    let ns = NSGraphicsContext(cgContext: ctx, flipped: false)
    NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ns
    let title = NSFont(name: "AvenirNextCondensed-Heavy", size: 74) ?? NSFont.boldSystemFont(ofSize: 66)
    let sub = NSFont(name: "AvenirNextCondensed-DemiBold", size: 34) ?? NSFont.boldSystemFont(ofSize: 30)
    NSAttributedString(string: "GREEN MOUNTAIN", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 540, y: 380))
    NSAttributedString(string: "EATS", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 540, y: 300))
    NSAttributedString(string: "CREEMEES, CIDER DONUTS & DINERS", attributes: [.font: sub, .foregroundColor: NSColor(srgbRed: 0.851, green: 0.643, blue: 0.255, alpha: 1)]).draw(at: NSPoint(x: 544, y: 250))
    NSGraphicsContext.restoreGraphicsState()
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
og("docs/og.png")
