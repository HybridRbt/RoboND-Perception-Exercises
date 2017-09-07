# Import PCL module
import pcl

# Load Point Cloud file
cloud = pcl.load_XYZRGB('tabletop.pcd')

# Voxel Grid filter
# Create a VoxelGrid filter object for out input point cloud
vox = cloud.make_voxel_grid_filter()

# choose a voxel (leaf) size
# LEAF_SIZE = 0.0001 # this is warned by the script to be too small
# LEAF_SIZE = 0.001 # same as above
LEAF_SIZE = 0.01  # no warning for this value, try a larger value
# LEAF_SIZE = 0.1 # this is too large to show any feature
# tried 0.01 ~ 0.05, 0.01 is the best

# Set voxel size
vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)

# call the filter funciton to obtain the resultant downsampled point cloud
cloud_filtered = vox.filter()
filename = 'voxel_downsampled.pcd'
pcl.save(cloud_filtered, filename)

# PassThrough filter
# Create a PassThrough filter objects
passthrough = cloud_filtered.make_passthrough_filter()

# Assign axis and range to the passthrough filter objects
filter_axis = 'z'
passthrough.set_filter_field_name(filter_axis)

# set the limits
# for the quiz in lesson 3-11
#axis_min = 0.8  # this removes the table
#axis_max = 2

#axis_min = 0.1  # this removes the objects on the table, leaves only the table
#axis_max = 0.8

#axis_min = 0  # this includes everything
#axis_max = 2

axis_min = 0.6  # this retains the table and the objects
axis_max = 1.1

passthrough.set_filter_limits(axis_min, axis_max)

# Finally, use the filter function to obtain the resultant point cloud
cloud_filtered = passthrough.filter()
filename = 'pass_through_filtered.pcd'
pcl.save(cloud_filtered, filename)

# RANSAC plane segmentation
# Create the segmentation object
seg = cloud_filtered.make_segmenter()

# Set the model you wish to filter
seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)

# Max distance for a point to be considered fitting the model
# For lesson 3-15 quiz 1
# max_distance = 1  # this includes everything
# max_distance = 0.1 # this removes the tall objects
max_distance = 0.01 # this leaves only the table
# max_distance = 0.001 # this might be unnessessarily high

seg.set_distance_threshold(max_distance)

# Call the segment function to obtain set of inlier indices and model coefficients
inliers, coefficients = seg.segment()

# Extract inliers
extracted_inliers = cloud_filtered.extract(inliers, negative=False)
filename = 'extracted_inliers.pcd'
pcl.save(extracted_inliers, filename)

# Extract outliers
extracted_outliers = cloud_filtered.extract(inliers, negative=True)
filename = 'extracted_outliers.pcd'
pcl.save(extracted_outliers, filename)

# Save pcd for table
# pcl.save(cloud, filename)


# Extract outliers


# Save pcd for tabletop objects
