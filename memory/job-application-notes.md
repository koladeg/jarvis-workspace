# Reusable Job Application Notes

_Last updated: 2026-05-04 09:46 UTC_

## React Native / Native Modules Evidence Bank

Use this section when applications ask about native modules, mobile platform integration, Expo dev-client constraints, or production debugging in React Native.

### Core positioning
Kolade has hands-on experience integrating native-backed modules into React Native applications, especially in logistics/transport products built at SIFAX, including the **Kargo Mobile Platform** and **Kago Driver Mobile Platform**.

He should be positioned as:
- strong in **integrating, configuring, debugging, and shipping** native-backed modules in production React Native apps
- comfortable with **Android/iOS platform differences**, permissions, SDK setup, and dependency issues
- **not** primarily positioned as someone whose main role is authoring large custom native modules from scratch in Java/Kotlin/Swift/Objective-C

### Native-backed modules / libraries actually referenced

#### Location and mapping
- `expo-location`
- `react-native-maps`
- `react-native-google-places-autocomplete`
- `react-native-google-maps-directions`

Use cases:
- live location access
- route display
- address search
- trip / navigation-related workflows

#### Push notifications and device services
- `expo-notifications`
- `expo-device`
- `expo-application`

Use cases:
- alerts / notifications
- device-level behavior
- runtime / app identification

#### Persistence and connectivity
- `@react-native-async-storage/async-storage`
- `@react-native-community/netinfo`

Use cases:
- session persistence
- offline-aware flows
- network state handling

#### Media / device access
- `expo-image-picker`

Use cases:
- image capture or selection flows

#### Animation / performance-sensitive UI
- `lottie-react-native`
- `react-native-reanimated`
- `react-native-gesture-handler`
- `react-native-screens`
- `react-native-pager-view`

Use cases:
- animations
- gesture-heavy UI
- performance-sensitive mobile interactions

#### Monitoring / diagnostics
- `@sentry/react-native`

Use cases:
- production diagnostics
- crash/error monitoring

#### Platform configuration dependencies
- Firebase-related native setup via `google-services.json`
- Expo dev-client / native runtime setup

Use cases:
- native configuration and SDK initialization
- cases where pure Expo Go support was not enough

### Strong example framing
A strong example is the logistics / driver workflow at SIFAX, where the app had to combine:
- real-time location
- maps and route handling
- connectivity state
- push notifications
- production reliability across devices

This is a useful example because it shows work that goes beyond plain JavaScript into:
- native permissions
- SDK initialization
- Android/iOS configuration
- device-specific behavior

### Recurring challenges to mention
- permissions management for location, notifications, and media access
- Android/iOS configuration differences
- build and dependency compatibility issues across React Native, Expo, Gradle/CocoaPods, Reanimated, Maps, or Sentry
- debugging inconsistent cross-platform behavior
- managing native-backed modules inside Expo / dev-client workflows when proper native builds were required

### Reusable answer pattern

#### Medium version
“Yes — I’ve integrated a number of native-backed modules into React Native applications, particularly in logistics/transport products I worked on at SIFAX, including the Kargo Mobile Platform and Kago Driver Mobile Platform.

Some of the main native-module use cases I’ve worked with include location and mapping features using expo-location, react-native-maps, react-native-google-places-autocomplete, and react-native-google-maps-directions for live location access, route display, address search, and trip/navigation workflows. I’ve also worked with push notifications and device-level services through expo-notifications, expo-device, and expo-application, as well as local persistence and connectivity-aware flows using AsyncStorage and NetInfo.

A good example of where this mattered was in driver and logistics workflows, where the app had to combine real-time location, maps, route handling, network-awareness, and notifications in a way that felt reliable in production. That kind of work goes beyond plain JavaScript because you’re dealing with native permissions, SDK initialization, Android/iOS configuration, and device-specific behavior.

Some recurring challenges I faced were permissions management, platform-specific configuration differences, dependency compatibility issues across React Native/Expo and native libraries, and debugging cases where something worked on Android but needed extra setup on iOS. So while I wouldn’t position myself as someone whose main role is building large custom native modules from scratch, I do have solid hands-on experience integrating, configuring, debugging, and shipping native modules inside React Native apps for real business use cases.”

#### Short version
“Yes — I’ve integrated several native-backed modules in React Native apps, especially in logistics products at SIFAX. That includes location/maps, notifications, connectivity-aware flows, media access, performance-sensitive UI libraries, Sentry, and Firebase-related native setup. The main challenges were permissions, Android/iOS setup differences, Expo/dev-client constraints, and dependency compatibility across native libraries. I’m strongest at integrating and shipping native-backed functionality reliably in production, even if I’m not primarily a custom native-module author.”

## Company-specific notes

### Charted Sea
- Role was a stretch relative to Kolade’s main frontend / React Native lane.
- Best positioning: strong TypeScript/JavaScript, debugging mindset, comfort with partially understood systems, tool-building interest.
- Submitted application email to `marc.plouhinec@chartedsea.com` with PDF CV on 2026-05-04.

### Tether
- Stronger lane than Charted Sea.
- Good emphasis areas:
  - React Native product delivery
  - production app reliability
  - native module integration
  - mobile platform debugging
  - remote collaboration
  - fintech-adjacent / operational product environments

## Reuse rule
Before writing future application answers, check this file first for:
- mobile / native module evidence
- reusable phrasing
- SIFAX logistics examples
- role-specific positioning notes
