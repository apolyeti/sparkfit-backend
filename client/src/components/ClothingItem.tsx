import type { SparkFitImage } from "@utils/types";
import Image from "next/image";

interface ClothingItemProps {
    key: string; // for mapping
    image: SparkFitImage;
}

export default function ClothingItem(ClothingItemProps: ClothingItemProps) {
    const { image } = ClothingItemProps;
    return (
        // make a card for each image
        <div className="flex flex-col items-center justify-center">
            <Image src={image.data} alt={image.name + " submitted by user"} width={200} height={200} />
            <p>{image.name}</p>
        </div>
    )
}
