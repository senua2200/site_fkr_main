import { VideoUse } from "../../HowUsagePageComponents/VideoUse";
import { VariantsUse } from "../../HowUsagePageComponents/VariantsUse";
import { ComfortUse } from "../../HowUsagePageComponents/ComfortUse";
import { StepsUse } from "../../HowUsagePageComponents/StepsUse";

export const HowUsagePage = () => {
    return (
        <>
            <VideoUse></VideoUse>
            <StepsUse></StepsUse>
            <VariantsUse></VariantsUse>
            <ComfortUse></ComfortUse>
        </>
    );
};