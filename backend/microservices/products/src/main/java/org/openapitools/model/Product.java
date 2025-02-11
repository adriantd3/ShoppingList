package org.openapitools.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

/**
 * Product
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Product {

    @NotNull
    @Schema(name = "id", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("id")
    private Integer id;

    @NotNull
    @Valid
    @Schema(name = "owner", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("owner")
    private UserInfo owner;

    @NotNull
    @Schema(name = "name", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("name")
    private String name;

    @NotNull
    @Schema(name = "category", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("category")
    private String Category;

    @NotNull
    @Schema(name = "image", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("image")
    private String image;

    @NotNull
    @Schema(name = "description", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("description")
    private String description;

    @NotNull
    @Schema(name = "timestamp", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("timestamp")
    @JsonFormat(shape = JsonFormat.Shape.STRING)
    private Instant timestamp;

    @NotNull
    @Schema(name = "user_generated", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("user_generated")
    private Boolean userGenerated;
}
