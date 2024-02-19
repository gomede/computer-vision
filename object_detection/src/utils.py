# Let's create the .txt files based on the provided annotations and content format

# Annotations provided by the user
annotations = """
20230728_100531-0-_jpg.rf.06dffff29051f7ec7f0a1e6866fdee24.jpg 283,258,433,367,0
20230728_100727-0-_jpg.rf.14b3d5cb44537c45b18bd891322ee0d4.jpg 276,228,365,345,0
20230728_100524_jpg.rf.23164b32b769e2749ba819590c2d8722.jpg 246,317,387,416,0
20230728_100721_jpg.rf.369e5dad7616892b42bdccdc94767311.jpg 274,254,384,387,0
20230728_100611_jpg.rf.41bae209d2371b012df751dde99d3598.jpg 182,250,341,361,0
20230728_100713_jpg.rf.3ffa7bde1fe0d055954f3af038e2852d.jpg 231,261,317,377,0
20230728_100729_jpg.rf.4ab17197d862570d2cf92345a06ea8bf.jpg 258,234,349,346,0
20230728_100626-0-_jpg.rf.550648b5fb2f0d0a44b5e30700a9d839.jpg 279,158,449,296,0
20230728_100716_jpg.rf.5b53fd04678e854091a54f5d5853a81d.jpg 245,135,349,270,0
20230728_100707_jpg.rf.5a74eea4ef174441e79c1e0ced7ad770.jpg 208,241,330,399,0
20230728_100612_jpg.rf.40aff9fbde9ac39e0f211cacbcf9793e.jpg 172,280,341,402,0
20230728_100703_jpg.rf.7e589ae21f3593bfcb99d124076ef241.jpg 196,229,304,377,0
20230728_100706-0-_jpg.rf.c96f78d34e2ba4b424c71764101c88e5.jpg 236,267,352,420,0
20230728_100713-0-_jpg.rf.e585ae1617ab2096ac02986afdc365c1.jpg 226,229,317,351,0
20230728_100543_jpg.rf.c18bd2cb2f50f68209ddeb0e343a30bd.jpg 222,288,379,394,0
20230728_100614-0-_jpg.rf.a336db9eb1acc8ed0aa542948937f6a0.jpg 142,239,326,376,0
20230728_100725-0-_jpg.rf.e7697e0a2536b9ac9b515b8250c8ce0f.jpg 290,227,374,335,0
20230728_100546_jpg.rf.6b125abcc5cf0d8b2f5966d4c30867c4.jpg 232,239,406,351,0
20230728_100533_jpg.rf.fd134a792720d66252073965d65bb577.jpg 313,266,452,374,0
""".strip().split('\n')

# Prepare to write to individual .txt files
annotation_dict = {}
for line in annotations:
    parts = line.split()
    file_name = parts[0].replace('.jpg', '.txt')
    bbox = parts[1].split(',')
    class_id = bbox[-1]
    x_center = (int(bbox[0]) + int(bbox[2])) / 2
    y_center = (int(bbox[1]) + int(bbox[3])) / 2
    width = int(bbox[2]) - int(bbox[0])
    height = int(bbox[3]) - int(bbox[1])
    # Assuming image dimensions are 640x640 for normalization
    normalized = f"{class_id} {x_center / 640:.6f} {y_center / 640:.6f} {width / 640:.6f} {height / 640:.6f}"
    if file_name not in annotation_dict:
        annotation_dict[file_name] = [normalized]
    else:
        annotation_dict[file_name].append(normalized)

# Write the annotations to text files
output_paths = []
for file_name, lines in annotation_dict.items():
    output_path = f"object_detection/outputs/valid_labes/{file_name}"
    with open(output_path, "w") as f:
        for line in lines:
            f.write(f"{line}\n")
    output_paths.append(output_path)

output_paths
