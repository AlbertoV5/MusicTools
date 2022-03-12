MusicTool

Collection of tools for data scraping, source separation and digital signal processing.


1. Source Separation uses Spleeter to batch-separate an entire folder and save the results in there.
2. Scrap tools is focused on downloading .mp4/.ogg from YouTube. It scraps osu! and Beast Saber.
3. Music Tool:
  - Use getRMS.py to store loudness arrays, downsampled, to a .npy file. Batch it.
  - Use compareRMS.py to compare one array to the rest and find the most similar one based on dot product.
  - To do: Replace comparing arrays with dot product to comparing with clustering for better results.
