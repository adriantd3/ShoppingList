package org.openapitools.dto;

import java.util.Objects;
import com.fasterxml.jackson.annotation.JsonProperty;

import javax.validation.constraints.*;
import io.swagger.v3.oas.annotations.media.Schema;


import javax.annotation.Generated;

/**
 * NewProduct
 */

@Generated(value = "org.openapitools.codegen.languages.SpringCodegen", date = "2025-02-05T18:53:31.285160+01:00[Europe/Madrid]", comments = "Generator version: 7.9.0")
public class NewProduct {

  private String name;

  private String image;

  private Integer categoryId;

  private String description;

  public NewProduct() {
    super();
  }

  /**
   * Constructor with only required parameters
   */
  public NewProduct(String name, String image, Integer categoryId, String description) {
    this.name = name;
    this.image = image;
    this.categoryId = categoryId;
    this.description = description;
  }

  public NewProduct name(String name) {
    this.name = name;
    return this;
  }

  /**
   * Get name
   * @return name
   */
  @NotNull 
  @Schema(name = "name", requiredMode = Schema.RequiredMode.REQUIRED)
  @JsonProperty("name")
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public NewProduct image(String image) {
    this.image = image;
    return this;
  }

  /**
   * Get image
   * @return image
   */
  @NotNull 
  @Schema(name = "image", requiredMode = Schema.RequiredMode.REQUIRED)
  @JsonProperty("image")
  public String getImage() {
    return image;
  }

  public void setImage(String image) {
    this.image = image;
  }

  public NewProduct categoryId(Integer categoryId) {
    this.categoryId = categoryId;
    return this;
  }

  /**
   * Get categoryId
   * @return categoryId
   */
  @NotNull 
  @Schema(name = "category_id", requiredMode = Schema.RequiredMode.REQUIRED)
  @JsonProperty("category_id")
  public Integer getCategoryId() {
    return categoryId;
  }

  public void setCategoryId(Integer categoryId) {
    this.categoryId = categoryId;
  }

  public NewProduct description(String description) {
    this.description = description;
    return this;
  }

  /**
   * Get description
   * @return description
   */
  @NotNull 
  @Schema(name = "description", requiredMode = Schema.RequiredMode.REQUIRED)
  @JsonProperty("description")
  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    NewProduct newProduct = (NewProduct) o;
    return Objects.equals(this.name, newProduct.name) &&
        Objects.equals(this.image, newProduct.image) &&
        Objects.equals(this.categoryId, newProduct.categoryId) &&
        Objects.equals(this.description, newProduct.description);
  }

  @Override
  public int hashCode() {
    return Objects.hash(name, image, categoryId, description);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class NewProduct {\n");
    sb.append("    name: ").append(toIndentedString(name)).append("\n");
    sb.append("    image: ").append(toIndentedString(image)).append("\n");
    sb.append("    categoryId: ").append(toIndentedString(categoryId)).append("\n");
    sb.append("    description: ").append(toIndentedString(description)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }
}

