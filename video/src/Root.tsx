import { Composition } from "remotion";
import { BootSequence } from "./BootSequence";
import { SignalField } from "./SignalField";
import { Arcade } from "./Arcade";
import { Catalogue } from "./Catalogue";
import T from "./timeline.json";

export const Root = () => (
  <>
    <Composition id="BootSequence" component={BootSequence} durationInFrames={T.boot.frames} fps={T.fps} width={1920} height={1080} />
    <Composition id="SignalField" component={SignalField} durationInFrames={T.signal.frames} fps={T.fps} width={1920} height={1080} />
    <Composition id="Arcade" component={Arcade} durationInFrames={T.arcade.frames} fps={T.fps} width={1920} height={1080} />
    <Composition id="Catalogue" component={Catalogue} durationInFrames={T.catalogue.frames} fps={T.fps} width={1920} height={1080} />
  </>
);
