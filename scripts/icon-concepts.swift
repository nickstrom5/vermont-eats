// Green Mountain Eats icon concepts (2026-11-05), drawn in the shared Eats Ranked style (state-prompts/ICON-STYLE.md): one flat, level,
// centred food on spruce #1E4D2B (the prompt's landscape palette), no backing shape, no text or texture, no maple leaf (it reads as
// Canada). Food hexes: creemee cream #F3E3C3, maple amber #C77A2A, waffle-cone tan #D9A441, jug white #F7F3EA, barn red #9E2A2B,
// cheddar orange #F2A33A, crust gold #E2B56B.
//   A  a maple creemee: a soft-serve swirl in three tiers on a waffle cone, front view
//   B  a maple syrup jug: a white jug with a ring handle and an amber label band, front view
//   C  a slice of apple pie with a slice of cheddar on top, side view
// Usage, from vt-eats/: swift scripts/icon-concepts.swift <out dir>   -> concept-{a,b,c}-1024.png
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let SPRUCE: UInt32 = 0x1E4D2B, CREAM: UInt32 = 0xF3E3C3, AMBER: UInt32 = 0xC77A2A, TAN: UInt32 = 0xD9A441, WHITE: UInt32 = 0xF7F3EA
let RED: UInt32 = 0x9E2A2B, CHEDDAR: UInt32 = 0xF2A33A, CRUST: UInt32 = 0xE2B56B

/// A: the maple creemee. CoreGraphics y-up, s = canvas size. Identical to make-brand.swift's creemee().
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

/// B: the syrup jug: a white body with an amber label band, shoulders to a short neck, a red cap and a ring handle at the neck.
func jug(_ c: CGContext, _ s: CGFloat) {
    func P(_ x: CGFloat, _ y: CGFloat) -> CGPoint { CGPoint(x: x * s, y: y * s) }
    c.setFillColor(rgb(WHITE))
    c.addPath(CGPath(roundedRect: CGRect(x: 0.245 * s, y: 0.18 * s, width: 0.46 * s, height: 0.46 * s), cornerWidth: 0.05 * s, cornerHeight: 0.05 * s, transform: nil)); c.fillPath()
    let sh = CGMutablePath()
    sh.move(to: P(0.245, 0.62)); sh.addLine(to: P(0.705, 0.62)); sh.addLine(to: P(0.535, 0.72)); sh.addLine(to: P(0.415, 0.72)); sh.closeSubpath()
    c.addPath(sh); c.fillPath()
    c.fill(CGRect(x: 0.415 * s, y: 0.70 * s, width: 0.12 * s, height: 0.10 * s))
    // the ring handle: a white ring off the neck
    c.setLineWidth(0.045 * s); c.setStrokeColor(rgb(WHITE))
    c.strokeEllipse(in: CGRect(x: 0.54 * s, y: 0.60 * s, width: 0.17 * s, height: 0.17 * s))
    // the cap and the label band
    c.setFillColor(rgb(RED)); c.fill(CGRect(x: 0.405 * s, y: 0.80 * s, width: 0.14 * s, height: 0.065 * s))
    c.setFillColor(rgb(AMBER)); c.fill(CGRect(x: 0.245 * s, y: 0.30 * s, width: 0.46 * s, height: 0.20 * s))
}

/// C: a slice of apple pie with cheddar: bottom crust, amber apple filling, a gold top crust, an orange cheddar slice on top.
func pie(_ c: CGContext, _ s: CGFloat) {
    func P(_ x: CGFloat, _ y: CGFloat) -> CGPoint { CGPoint(x: x * s, y: y * s) }
    // side view of a wedge: the point at the left, the back crust at the right
    c.setFillColor(rgb(CRUST)); c.fill(CGRect(x: 0.15 * s, y: 0.30 * s, width: 0.70 * s, height: 0.06 * s))
    c.setFillColor(rgb(AMBER)); c.fill(CGRect(x: 0.15 * s, y: 0.36 * s, width: 0.70 * s, height: 0.16 * s))
    let top = CGMutablePath()
    top.move(to: P(0.15, 0.52)); top.addLine(to: P(0.85, 0.52)); top.addLine(to: P(0.85, 0.60)); top.addLine(to: P(0.22, 0.56)); top.closeSubpath()
    c.setFillColor(rgb(CRUST)); c.addPath(top); c.fillPath()
    c.fill(CGRect(x: 0.78 * s, y: 0.30 * s, width: 0.07 * s, height: 0.34 * s))   // the raised back crust
    c.setFillColor(rgb(CHEDDAR)); c.fill(CGRect(x: 0.36 * s, y: 0.59 * s, width: 0.36 * s, height: 0.10 * s))
}

func render(_ n: Int, _ path: String, _ draw: (CGContext, CGFloat) -> Void) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(SPRUCE)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n))
    draw(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "playbook/brand"
render(1024, out + "/concept-a-1024.png", creemee)
render(1024, out + "/concept-b-1024.png", jug)
render(1024, out + "/concept-c-1024.png", pie)
