FROM rust:latest as builder
WORKDIR /usr/src/potato_plant_replay
ENV CARGO_HOME=/etc/rust-cache
COPY . .
RUN cargo install --path .

FROM ubuntu:22.04

COPY --from=builder /usr/local/cargo/bin/potato_plant_replay /usr/local/bin/
COPY www /usr/local/bin/www

RUN rm -rf /var/lib/apt/lists/*
CMD ["/bin/sh", "-c", "potato_plant_replay"]

